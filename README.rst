LESSCPY
=======

.. image:: https://travis-ci.org/lesscpy/lesscpy.png?branch=master
        :target: https://travis-ci.org/lesscpy/lesscpy

.. image:: https://coveralls.io/repos/lesscpy/lesscpy/badge.png
        :target: https://coveralls.io/r/lesscpy/lesscpy

.. image:: https://pypip.in/d/lesscpy/badge.png
        :target: https://pypi.python.org/pypi/lesscpy

.. image:: https://pypip.in/v/lesscpy/badge.png
        :target: https://pypi.python.org/pypi/lesscpy

.. image:: https://pypip.in/wheel/lesscpy/badge.png
        :target: https://pypi.python.org/pypi/lesscpy
        :alt: Wheel Status

.. image:: https://pypip.in/license/lesscpy/badge.png
        :target: https://pypi.python.org/pypi/lesscpy
        :alt: License

Python LESS Compiler.

A compiler written in Python for the LESS language. For those of us not willing
or able to have node.js installed in our environment. Not all features of LESS
are supported (yet). Some features wil probably never be supported (JavaScript
evaluation). This program uses PLY (Python Lex-Yacc) to tokenize / parse the
input and is considerably slower than the NodeJS compiler. The plan is to
utilize this to build in proper syntax checking and perhaps YUI compressing.

This is an early version, so you are likly to find bugs.

For more information on LESS:
  http://lesscss.org/ or https://github.com/cloudhead/less.js
 
Development files:
  https://github.com/lesscpy/lesscpy


Supported features
------------------

- Variables
- String interpolation
- Mixins (nested, calls, closures, recursive)
- Guard expressions
- Parametered mixins (class / id)
- @arguments
- Nesting
- Escapes ~/e()
- Expressions
- Keyframe blocks
- Color functions (lighten, darken, saturate, desaturate, spin, hue, mix,
                   saturation, lightness)
- Other functions (round, increment, decrement, format '%(', ...)
- Keyframe blocks


Differences from less.js
------------------------

- All colors are auto-formatted to #nnnnnn. eg, #f7e923
- Does not preserve CSS comments


Not supported yet
-----------------

- Interpolation in imports.
- Interpolation in property names when variable is an expression.
- Interpolation in property names when merged with '+'.
- Variable name can not be a single '-' (dash) character.


Not supported
-------------

- JavaScript evaluation
 

Requirements
------------

- Python 2.6, 2.7, or 3.3
- ply (Python Lex-Yacc) (check requirements.txt)
 

Installation
------------

To install lesscpy from the `Python Package Index`_, simply:

.. code-block:: bash

    $ pip install lesscpy

To do a local system-wide install:

.. code-block:: bash

    python setup.py install
 
Or simply place the package into your Python path. Or rather use packages
provided by your distribution (openSUSE has them at least).


Compiler script Usage
---------------------
 
.. code-block:: text

    usage: lesscpy [-h] [-v] [-I INCLUDE] [-V] [-x] [-X] [-t] [-s SPACES] [-o OUT]
                   [-r] [-f] [-m] [-D] [-g] [-S] [-L] [-N]
                   target

    LessCss Compiler

    positional arguments:
      target                less file or directory

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -I INCLUDE, --include INCLUDE
                            Included less-files (comma separated)
      -V, --verbose         Verbose mode

    Formatting options:
      -x, --minify          Minify output
      -X, --xminify         Minify output, no end of block newlines
      -t, --tabs            Use tabs
      -s SPACES, --spaces SPACES
                            Number of startline spaces (default 2)

    Directory options:
      Compiles all \*.less files in directory that have a newer timestamp than
      it's css file.

      -o OUT, --out OUT     Output directory
      -r, --recurse         Recursive into subdirectorys
      -f, --force           Force recompile on all files
      -m, --min-ending      Add '.min' into output filename. eg, name.min.css
      -D, --dry-run         Dry run, do not write files

    Debugging:
      -g, --debug           Debugging information
      -S, --scopemap        Scopemap
      -L, --lex-only        Run lexer on target
      -N, --no-css          No css output


Development
-----------

You can create a virtual environment in '.venv' directory.

Tests are copied from original Less project as less and css files and places
in `test` directory.

You can run the test for a single file using the following command.
For file `test/less/lazy-eval.less` you will run::

  nosetests test.test_less:LessTestCase.test_less_lazy-eval

There are also normal unit tests in `test` directory.


License
-------

See the LICENSE file


.. _`Python Package Index`: https://pypi.python.org/pypi/rapport

