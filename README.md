[![PyPI](https://img.shields.io/pypi/v/lazy_loader)](https://pypi.org/project/lazy_loader/)
[![Test status](https://github.com/scientific-python/lazy_loader/workflows/test/badge.svg?branch=main)](https://github.com/scientific-python/lazy_loader/actions?query=workflow%3A%22test%22)
[![Test coverage](https://codecov.io/gh/scientific-python/lazy_loader/branch/main/graph/badge.svg)](https://app.codecov.io/gh/scientific-python/lazy_loader/branch/main)

`lazy_loader` makes it easy to load subpackages and functions on demand.

## Motivation

1. Allow subpackages to be made visible to users without incurring import costs.
2. Allow external libraries to be imported only when used, improving import times.

For a more detailed discussion, see [the SPEC](https://scientific-python.org/specs/spec-0001/).

## Installation

```
pip install -U lazy_loader
```

## Usage

### Lazily load subpackages

Consider the `__init__.py` from [scikit-image](https://scikit-image.org):

```python
subpackages = [
    ...,
    'filters',
    ...
]

import lazy_loader as lazy
__getattr__, __dir__, _ = lazy.attach(__name__, subpackages)
```

You can now do:

```python
import skimage as ski
ski.filters.gaussian(...)
```

The `filters` subpackages will only be loaded once accessed.

### Lazily load subpackages and functions

Consider `skimage/filters/__init__.py`:

```python
from ..util import lazy

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submodules=['rank'],
    submod_attrs={
        '_gaussian': ['gaussian', 'difference_of_gaussians'],
        'edges': ['sobel', 'scharr', 'prewitt', 'roberts',
                  'laplace', 'farid']
    }
)
```

The above is equivalent to:

```python
from . import rank
from ._gaussian import gaussian, difference_of_gaussians
from .edges import (sobel, scharr, prewitt, roberts,
                    laplace, farid)
```

Except that all subpackages (such as `rank`) and functions (such as `sobel`) are loaded upon access.

### Lazily load subpackages and functions from type stubs

Because static type checkers and IDEs will likely be unable to find your
dynamically declared imports, you can use a [type
stub](https://mypy.readthedocs.io/en/stable/stubs.html) (`.pyi` file) to declare
the imports. However, if used with the above pattern, this results in code
duplication, as you now need to declare your submodules and attributes in two places.

You can infer the `submodules` and `submod_attrs` arguments (explicitly provided
above to `lazy.attach`) from a stub adjacent to the `.py` file by using the
`lazy.attach_stub` function.

Carrying on with the example above:

The `skimage/filters/__init__.py` module would be declared as such:

```python
from ..util import lazy

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
```

... and the adjacent `skimage/filters/__init__.pyi` stub would contain:

```python
from . import rank
from ._gaussian import gaussian, difference_of_gaussians
from .edges import (sobel, scharr, prewitt, roberts,
                    laplace, farid)
```

Note that in order for this to work, you must be sure to include the `.pyi`
files in your package distribution. For example, with setuptools, you would need
to [set the `package_data`
option](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#package-data)
to include `*.pyi` files.

### Early failure

With lazy loading, missing imports no longer fail upon loading the
library. During development and testing, you can set the `EAGER_IMPORT`
environment variable to disable lazy loading.

### External libraries

The `lazy.attach` function discussed above is used to set up package
internal imports.

Use `lazy.load` to lazily import external libraries:

```python
linalg = lazy.load('scipy.linalg')  # `linalg` will only be loaded when accessed
```

You can also ask `lazy.load` to raise import errors as soon as it is called:

```
linalg = lazy.load('scipy.linalg', error_on_import=True)
```
