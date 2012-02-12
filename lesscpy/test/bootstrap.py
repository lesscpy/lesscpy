"""
    Test bootstrap module. For flexible testing.
"""
import os
import sys

here = os.path.dirname(__file__)
path = os.path.abspath(here)
while os.path.dirname(path) != path:
    if os.path.exists(os.path.join(path, 'lesscpy', '__init__.py')):
        sys.path.insert(0, path)
        break
    path = os.path.dirname(path)