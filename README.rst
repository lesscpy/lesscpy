LESSCPY
=======

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
  https://github.com/robotis/Lesscpy
 

Requirements
------------

- Python 2.6 or 2.7
- ply (Python Lex-Yacc)

For more information on ply:
  http://www.dabeaz.com/ply/
 

Installation
------------

.. code-block:: bash

    python setup.py install
 
Or simply place the package into your Python path.


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


Supported features
------------------

- Variables
- String interpolation
- Mixins
- mixins (Nested)
- mixins (Nested (Calls))
- mixins (closures)
- mixins (recursive)
- Guard expressions
- Parametered mixins (class)
- Parametered mixins (id)
- @arguments
- Nesting
- Escapes ~/e()
- Expressions
- Keyframe blocks
- Color functions:

  - lighten
  - darken
  - saturate
  - desaturate
  - spin
  - hue
  - mix
  - saturation
  - lightness

- Other functions:

  - round
  - increment
  - decrement
  - format '%('
  - add
  - iscolor
  - isnumber
  - isurl
  - isstring
  - iskeyword

- Keyframe blocks


Differences from less.js
------------------------

- All MS filters and other strange vendor constructs must be escaped
- All colors are auto-formatted to #nnnnnn. eg, #f7e923
- Does not preserve css comments


Not supported
-------------

- JavaScript evaluation


License
-------

See the LICENSE file
