"""
    lesscpy reported issues tests.
"""
import unittest

from test.core import find_and_load_cases


class IssuesTestCase(unittest.TestCase):
    pass


find_and_load_cases(
    IssuesTestCase,
    less_dir='less/issues',
    css_dir='css/issues',
    css_minimized=False)
