# LESSCPY

[![Build Status](https://github.com/lesscpy/lesscpy/actions/workflows/main.yml/badge.svg)](https://github.com/lesscpy/lesscpy/actions/workflows/main.yml)
[![Coverage Status](https://coveralls.io/repos/lesscpy/lesscpy/badge.png)](https://coveralls.io/r/lesscpy/lesscpy)
[![PyPI Downloads](https://img.shields.io/pypi/dm/lesscpy.svg)](https://pypi.python.org/pypi/lesscpy)
[![PyPI Version](https://img.shields.io/pypi/v/lesscpy.svg)](https://pypi.python.org/pypi/lesscpy)
[![Wheel Status](https://img.shields.io/pypi/wheel/lesscpy.svg)](https://pypi.python.org/pypi/lesscpy)
[![License](https://img.shields.io/pypi/l/lesscpy.svg)](https://pypi.python.org/pypi/lesscpy)

Python LESS Compiler.

A compiler written in Python for the LESS language. For those of us not willing
or able to have node.js installed in our environment. Not all features of LESS
are supported. Some features will probably never be supported (JavaScript
evaluation). This program uses PLY (Python Lex-Yacc) to tokenize / parse the
input and is considerably slower than the Node.js compiler.

For more information on LESS:
- http://lesscss.org/
- https://github.com/cloudhead/less.js

Development files:
- https://github.com/lesscpy/lesscpy

## Supported features

- Variables
- String interpolation
- Mixins (nested, calls, closures, recursive)
- Guard expressions
- Parametered mixins (class / id)
- `@arguments`
- Nesting
- Escapes `~/e()`
- Expressions
- Keyframe blocks
- Color functions (lighten, darken, saturate, desaturate, spin, hue, mix, saturation, lightness)
- Other functions (round, increment, decrement, format `'%(...)`)

## Differences from less.js

- All colors are auto-formatted to `#nnnnnn` (for example, `#f7e923`)
- Does not preserve CSS comments

## Not supported

- JavaScript evaluation

## Requirements

- Python 3.11+
- `pip`

## Installation

Install from PyPI:

```bash
pip install lesscpy
```

## Local setup

Create and activate a virtual environment, then install test dependencies from `pyproject.toml`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

## Build

Build source and wheel distributions:

```bash
python -m pip install --upgrade build
python -m build
```

Artifacts are created in `dist/`.

## Test

Run unit tests:

```bash
pytest -v
```

Run lint checks:

```bash
flake8
```

## Using tox

`tox` is useful for running the project test workflow in isolated environments and for reproducing the same multi-version checks used in CI.

Run all configured environments:

```bash
python -m pip install -e ".[tox]"
tox
```

Run a single environment:

```bash
tox -e py3.12
tox -e flake8
```

## Compiler script usage

```text
usage: lesscpy [-h] [-v] [-I INCLUDE] [-V] [-C] [-x] [-X] [-t] [-s SPACES]
               [-o OUT] [-r] [-f] [-m] [-D] [-g] [-S] [-L] [-N]
               target [output]
```

## Python usage

```python
from io import StringIO
import lesscpy

print(lesscpy.compile(StringIO("a { border-width: 2px * 3; }"), minify=True))
```

Output:

```text
a{border-width:6px;}
```

## License

See the `LICENSE` file.