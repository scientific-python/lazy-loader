import lazy_loader as lazy

with lazy.lazy_imports():
    from .some_func import some_func
    from . import some_mod, nested_pkg
