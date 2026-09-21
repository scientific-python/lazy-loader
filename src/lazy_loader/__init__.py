"""
lazy_loader
===========

Makes it easy to load subpackages and functions on demand.
"""

import _thread
import importlib
import os
import sys
import types

__version__ = "0.6rc1.dev0"
__all__ = ["attach", "attach_stub", "load"]


# Same lock type as threading.Lock(), without the threading import cost
threadlock = _thread.allocate_lock()


class _ShadowGuardModule(types.ModuleType):
    """Module type to protect function attributes from being overwritten.

    When a function has the same name as the submodule it resides in
    (e.g. a ``max_tree`` function defined in ``max_tree.py``),
    importing that submodule causes the import machinery to call
    ``setattr(pkg, "max_tree", <submodule>)``.  That updates the
    package ``__dict__``, preventing ``__getattr__`` from ever
    resolving the name to the function again. The same problem occurs
    when ``x`` is defined in ``x/sub.py``.

    This subclass suppresses those dictionary updates (only in the
    shadowing case).

    We track the set of protected names in the ``__lazy_shadowed__``
    attr.

    """

    def __setattr__(self, name, value):
        shadowed = self.__dict__.get("__lazy_shadowed__")
        if (
            shadowed is not None
            and name in shadowed
            # Is it trying to set this attribute to the system module?
            and value is sys.modules.get(f"{self.__name__}.{name}")
        ):
            return
        super().__setattr__(name, value)


# PEP 810 explicit lazy imports.  The syntax is not available on every 3.15
# build, so detect it rather than comparing version numbers.
try:
    compile("lazy import sys", "<lazy_loader probe>", "exec")
except SyntaxError:
    _NATIVE_LAZY_IMPORTS = False
else:
    _NATIVE_LAZY_IMPORTS = True


def _attach_native(package_name, submodules, submod_attrs):
    """Bind native lazy import proxies (PEP 810) in the package namespace.

    Names already bound in the package namespace are left untouched.  Where
    proxies cannot be bound, the names stay unbound and the caller's
    ``__getattr__`` provides the lazy behavior instead.
    """
    package = sys.modules.get(package_name)
    if package is None:
        # Not inside the package's import; cannot bind proxies in its
        # namespace.
        return

    # Since the names are embedded in generated import statements below,
    # ensure they are identifiers and not arbitrary code.
    names = [package_name, *submodules, *submod_attrs]
    names.extend(attr for attrs in submod_attrs.values() for attr in attrs)
    if not all(part.isidentifier() for name in names for part in name.split(".")):
        return

    pkg_dict = vars(package)

    # Absolute imports, like the classic __getattr__ mechanism uses, so that
    # no relative-import resolution (via __spec__ or __package__) is needed.
    # `submodules` is a set, so sort it for a reproducible statement order;
    # `submod_attrs` keeps its own order, under which a name listed for
    # several modules resolves to the last one, as in __getattr__.
    lines = [
        f"lazy from {package_name} import {name}"
        for name in sorted(submodules)
        if name not in pkg_dict
    ]
    for mod, attrs in submod_attrs.items():
        new_attrs = [a for a in attrs if a not in pkg_dict and a not in submodules]
        if new_attrs:
            lines.append(
                f"lazy from {package_name}.{mod} import {', '.join(new_attrs)}"
            )

    if not lines:
        return

    try:
        code = compile(
            "\n".join(lines), f"<lazy_loader.attach {package_name!r}>", "exec"
        )
    except SyntaxError:
        # A submodule or attribute name that is not expressible as import
        # syntax (e.g., a reserved keyword).
        return

    # exec() inserts __builtins__ into the namespace it is given; leave the
    # package namespace as it was found.
    had_builtins = "__builtins__" in pkg_dict
    exec(code, pkg_dict)
    if not had_builtins:
        pkg_dict.pop("__builtins__", None)


def attach(package_name, submodules=None, submod_attrs=None):
    """Attach lazily loaded submodules, functions, or other attributes.

    Typically, modules import submodules and attributes as follows::

      import mysubmodule
      import anothersubmodule

      from .foo import someattr

    The idea is to replace a package's `__getattr__`, `__dir__`, and
    `__all__`, such that all imports work exactly the way they would
    with normal imports, except that the import occurs upon first use.

    The typical way to call this function, replacing the above imports, is::

      __getattr__, __dir__, __all__ = lazy.attach(
          __name__, ["mysubmodule", "anothersubmodule"], {"foo": ["someattr"]}
      )

    On Python 3.15 and newer, this delegates to the interpreter's native
    lazy import mechanism (PEP 810) whenever possible.

    Parameters
    ----------
    package_name : str
        Typically use ``__name__``.
    submodules : set
        List of submodules to attach.
    submod_attrs : dict
        Dictionary of submodule -> list of attributes / functions.
        These attributes are imported as they are used.

    Returns
    -------
    __getattr__, __dir__, __all__

    """
    if submod_attrs is None:
        submod_attrs = {}

    if submodules is None:
        submodules = set()
    else:
        submodules = set(submodules)

    attr_to_modules = {
        attr: mod for mod, attrs in submod_attrs.items() for attr in attrs
    }

    __all__ = sorted(submodules | attr_to_modules.keys())

    def __getattr__(name):
        if name in submodules:
            attr = importlib.import_module(f"{package_name}.{name}")
        elif name in attr_to_modules:
            submod_path = f"{package_name}.{attr_to_modules[name]}"
            submod = importlib.import_module(submod_path)
            attr = getattr(submod, name)
        else:
            raise AttributeError(f"No {package_name} attribute {name}")

        # Cache the resolved value on the package so that subsequent
        # accesses bypass __getattr__; this also ensures an attribute
        # shadows a same-named submodule.
        pkg = sys.modules.get(package_name)
        if pkg is not None:
            pkg.__dict__[name] = attr

        return attr

    def __dir__():
        return __all__.copy()

    # When a function has the same name as a module the import
    # machinery needs to load along the way to accessing it
    # (e.g. `max_tree` from `max_tree.py`, or `x` from `x/sub.py`), a
    # side-effect of it loading that module is overwriting the package
    # attribute (so it points to the module, i.e. to `max_tree` or `x`
    # the module), shadowing the function (see _ShadowGuardModule).
    #
    # Record affected cases and, only in those cases, swap in the
    # guarding module type.
    shadowed = {
        attr for attr, mod in attr_to_modules.items() if attr == mod.split(".")[0]
    }
    if shadowed:
        pkg = sys.modules.get(package_name)
        # Only touch plain package modules (or our own wrapper) --- we
        # don't want to mess with custom module classes.
        if type(pkg) in (types.ModuleType, _ShadowGuardModule):
            pkg.__dict__["__lazy_shadowed__"] = (
                pkg.__dict__.get("__lazy_shadowed__", set()) | shadowed
            )
            if type(pkg) is types.ModuleType:
                pkg.__class__ = _ShadowGuardModule

    eager_import = os.environ.get("EAGER_IMPORT", "") not in ("0", "")
    if eager_import:
        for attr in set(attr_to_modules.keys()) | submodules:
            __getattr__(attr)
    elif _NATIVE_LAZY_IMPORTS:
        # On Python 3.15+, delegate to native lazy imports (PEP 810) where
        # possible.  The proxies are bound directly in the package namespace,
        # so the returned __getattr__ is then only consulted for unknown
        # names.  If native binding is not possible (e.g. `package_name` is
        # not an imported module), the classic __getattr__ mechanism above
        # provides the lazy behavior as before.
        _attach_native(package_name, submodules, submod_attrs)

    return __getattr__, __dir__, __all__.copy()


class DelayedImportErrorModule(types.ModuleType):
    def __init__(self, frame_data, *args, message, **kwargs):
        self.__frame_data = frame_data
        self.__message = message
        super().__init__(*args, **kwargs)

    def __getattr__(self, x):
        fd = self.__frame_data
        raise ModuleNotFoundError(
            f"{self.__message}\n\n"
            "This error is lazily reported, having originally occurred in\n"
            f"  File {fd['filename']}, line {fd['lineno']}, in {fd['function']}\n\n"
            f"----> {''.join(fd['code_context'] or '').strip()}"
        )


def load(fullname, *, require=None, error_on_import=False, suppress_warning=False):
    """Return a lazily imported proxy for a module.

    We often see the following pattern::

      def myfunc():
          import numpy as np
          np.norm(...)
          ....

    Putting the import inside the function prevents, in this case,
    `numpy`, from being imported at function definition time.
    That saves time if `myfunc` ends up not being called.

    This `load` function returns a proxy module that, upon access, imports
    the actual module.  So the idiom equivalent to the above example is::

      np = lazy.load("numpy")

      def myfunc():
          np.norm(...)
          ....

    The initial import time is fast because the actual import is delayed
    until the first attribute is requested. The overall import time may
    decrease as well for users that don't make use of large portions
    of your library.

    Warning
    -------
    While lazily loading *sub*packages technically works, it causes the
    package (that contains the subpackage) to be eagerly loaded even
    if the package is already lazily loaded.
    So, you probably shouldn't use subpackages with this `load` feature.
    Instead you should encourage the package maintainers to use the
    `lazy_loader.attach` to make their subpackages load lazily.

    Parameters
    ----------
    fullname : str
        The full name of the module or submodule to import.  For example::

          sp = lazy.load("scipy")  # import scipy as sp

    require : str
        A dependency requirement as defined in PEP-508.  For example::

          "numpy >=1.24"

        If defined, the proxy module will raise an error if the installed
        version does not satisfy the requirement.

    error_on_import : bool
        Whether to postpone raising import errors until the module is accessed.
        If set to `True`, import errors are raised as soon as `load` is called.

    suppress_warning : bool
        Whether to prevent emitting a warning when loading subpackages.
        If set to `True`, no warning will occur.

    Returns
    -------
    pm : importlib.util._LazyModule
        Proxy module.  Can be used like any regularly imported module.
        Actual loading of the module occurs upon first attribute request.

    """
    with threadlock:
        module = sys.modules.get(fullname)
        have_module = module is not None

        # Most common, short-circuit
        if have_module and require is None:
            return module

        import importlib.util

        if not suppress_warning and "." in fullname:
            import warnings

            msg = (
                "subpackages can technically be lazily loaded, but it causes the "
                "package to be eagerly loaded even if it is already lazily loaded. "
                "So, you probably shouldn't use subpackages with this lazy feature."
            )
            warnings.warn(msg, RuntimeWarning)

        spec = None

        if not have_module:
            spec = importlib.util.find_spec(fullname)
            have_module = spec is not None

        if not have_module:
            not_found_message = f"No module named '{fullname}'"
        elif require is not None:
            try:
                have_module = _check_requirement(require)
            except ModuleNotFoundError as e:
                raise ValueError(
                    f"Found module '{fullname}' but cannot test "
                    "requirement '{require}'. "
                    "Requirements must match distribution name, not module name."
                ) from e

            not_found_message = f"No distribution can be found matching '{require}'"

        if not have_module:
            if error_on_import:
                raise ModuleNotFoundError(not_found_message)
            import inspect

            parent = inspect.stack()[1]
            frame_data = {
                "filename": parent.filename,
                "lineno": parent.lineno,
                "function": parent.function,
                "code_context": parent.code_context,
            }
            del parent
            return DelayedImportErrorModule(
                frame_data,
                "DelayedImportErrorModule",
                message=not_found_message,
            )

        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            sys.modules[fullname] = module

            loader = importlib.util.LazyLoader(spec.loader)
            loader.exec_module(module)

    return module


def _check_requirement(require: str) -> bool:
    """Verify that a package requirement is satisfied

    If the package is required, a ``ModuleNotFoundError`` is raised
    by ``importlib.metadata``.

    Parameters
    ----------
    require : str
        A dependency requirement as defined in PEP-508

    Returns
    -------
    satisfied : bool
        True if the installed version of the dependency matches
        the specified version, False otherwise.
    """
    import importlib.metadata

    import packaging.requirements

    req = packaging.requirements.Requirement(require)
    return req.specifier.contains(
        importlib.metadata.version(req.name),
        prereleases=True,
    )


def attach_stub(package_name: str, filename: str):
    """Attach lazily loaded submodules, functions from a type stub.

    This is a variant on ``attach`` that will parse a `.pyi` stub file to
    infer ``submodules`` and ``submod_attrs``. This allows static type checkers
    to find imports, while still providing lazy loading at runtime.

    Parameters
    ----------
    package_name : str
        Typically use ``__name__``.
    filename : str
        Path to `.py` file which has an adjacent `.pyi` file.
        Typically use ``__file__``.

    Returns
    -------
    __getattr__, __dir__, __all__
        The same output as ``attach``.

    Raises
    ------
    ValueError
        If a stub file is not found for `filename`, or if the stubfile is formmated
        incorrectly (e.g. if it contains an relative import from outside of the module)
    """
    import ast

    class _StubVisitor(ast.NodeVisitor):
        """AST visitor to parse a stub file for submodules and submod_attrs."""

        def __init__(self):
            self._submodules = set()
            self._submod_attrs = {}

        def visit_ImportFrom(self, node: ast.ImportFrom):
            if node.level != 1:
                raise ValueError(
                    "Only within-module imports are supported (`from .* import`)"
                )
            if node.module:
                attrs: list = self._submod_attrs.setdefault(node.module, [])
                aliases = [alias.name for alias in node.names]
                if "*" in aliases:
                    raise ValueError(
                        "lazy stub loader does not support star import "
                        f"`from {node.module} import *`"
                    )
                attrs.extend(aliases)
            else:
                self._submodules.update(alias.name for alias in node.names)

    stubfile = (
        filename if filename.endswith("i") else f"{os.path.splitext(filename)[0]}.pyi"
    )

    if not os.path.exists(stubfile):
        raise ValueError(f"Cannot load imports from non-existent stub {stubfile!r}")

    with open(stubfile) as f:
        stub_node = ast.parse(f.read())

    visitor = _StubVisitor()
    visitor.visit(stub_node)
    return attach(package_name, visitor._submodules, visitor._submod_attrs)
