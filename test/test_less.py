"""
    lesscpy LESS tests.
"""
import unittest

from test.core import find_and_load_cases


class LessTestCase(unittest.TestCase):
    pass


find_and_load_cases(LessTestCase, less_dir='less', css_dir='css')
