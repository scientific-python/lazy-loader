import lazy_loader as lazy

from . import nested_mod_eager

with lazy.lazy_imports():
    from . import nested_mod_lazy
