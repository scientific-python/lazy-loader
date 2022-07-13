from lazy_loader import lazy_import

with lazy_import():
    from . import some_func  # noqa: F401
