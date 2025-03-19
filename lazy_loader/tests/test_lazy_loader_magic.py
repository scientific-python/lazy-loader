import importlib
import sys
import types

import lazy_loader as lazy
import pytest


def test_lazy_import_basics():
    with lazy.lazy_imports():
        import math

    with pytest.raises(ImportError):
        with lazy.lazy_imports():
            import anything_not_real

    # Now test that accessing attributes does what it should
    assert math.sin(math.pi) == pytest.approx(0, 1e-6)


def test_lazy_import_subpackages():
    with lazy.lazy_imports():
        import html.parser as hp
    assert "html" in sys.modules
    assert type(sys.modules["html"]) == type(pytest)
    assert isinstance(hp, importlib.util._LazyModule)
    assert "html.parser" in sys.modules
    assert sys.modules["html.parser"] == hp


def test_lazy_import_impact_on_sys_modules():
    with lazy.lazy_imports():
        import math

    with pytest.raises(ImportError):
        with lazy.lazy_imports():
            import anything_not_real

    assert isinstance(math, types.ModuleType)
    assert "math" in sys.modules
    assert "anything_not_real" not in sys.modules

    # only do this if numpy is installed
    pytest.importorskip("numpy")
    with lazy.lazy_imports():
        import numpy as np
    assert isinstance(np, types.ModuleType)
    assert "numpy" in sys.modules

    np.pi  # trigger load of numpy

    assert isinstance(np, types.ModuleType)
    assert "numpy" in sys.modules


def test_lazy_import_nonbuiltins():
    with lazy.lazy_imports():
        import numpy as np
        import scipy as sp

    assert np.sin(np.pi) == pytest.approx(0, 1e-6)


def test_attach_same_module_and_attr_name():
    from lazy_loader.tests import fake_pkg_magic

    # Grab attribute twice, to ensure that importing it does not
    # override function by module
    assert isinstance(fake_pkg_magic.some_func, types.FunctionType)
    assert isinstance(fake_pkg_magic.some_func, types.FunctionType)

    # Ensure imports from submodule still work
    from lazy_loader.tests.fake_pkg_magic.some_func import some_func

    assert isinstance(some_func, types.FunctionType)
