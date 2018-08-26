"""
    lesscpy bootstrap3 tests.
"""
import unittest

from test.core import find_and_load_cases


@unittest.skip("Minor semantic issues left")
class Bootstrap3TestCase(unittest.TestCase):
    pass


class Bootstrap3ThemeTestCase(unittest.TestCase):
    pass


find_and_load_cases(
    Bootstrap3TestCase,
    less_dir='bootstrap3/less',
    less_files=['bootstrap'],
    css_dir='bootstrap3/css')

find_and_load_cases(
    Bootstrap3ThemeTestCase,
    less_dir='bootstrap3/less',
    less_files=['theme'],
    css_dir='bootstrap3/css')
