"""
    lesscpy bootstrap3 tests.
"""
import unittest

from test.core import find_and_load_cases


class FontAwesomeTestCase(unittest.TestCase):
    pass


find_and_load_cases(FontAwesomeTestCase,
                    less_dir='font_awesome/less',
                    less_files=['font-awesome'],
                    css_dir='font_awesome/css')
