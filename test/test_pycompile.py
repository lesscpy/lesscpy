"""
Test the high-level compile function

"""
import unittest

from six import StringIO

from lesscpy import compile


class TestCompileFunction(unittest.TestCase):
    """
    Unit tests for compile
    """

    def test_compile(self):
        """
        It can compile input from a file-like object
        """

        output = compile(StringIO("a { border-width: 2px * 3; }"), minify=True)
        self.assertEqual(output, "a{border-width:6px;}");
