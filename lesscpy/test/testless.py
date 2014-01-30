"""
    lesscpy tests.
"""
import unittest
import os
import glob

from bootstrap import create_test, TestCase


_less_path = os.path.join(os.path.dirname(__file__), 'less')
_css_path = os.path.join(os.path.dirname(__file__), 'css')


LESS = glob.glob(os.path.join(_less_path, '*.less'))
for less in LESS:
    lessf = less.split('.')[0].split('/')[-1]
    css = os.path.join(_css_path, lessf + '.css')
    mincss = os.path.join(_css_path, lessf + '.min.css')
    test_method = create_test((less, css, mincss))
    test_method.__name__ = 'test_%s' % "_".join(reversed(os.path.basename(less).split('.')))
    setattr(TestCase, test_method.__name__, test_method)


if __name__ == "__main__":
    unittest.main()
