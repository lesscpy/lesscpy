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

    def test_compile_from_stream(self):
        """
        It can compile input from a file-like object
        """

        output = compile(StringIO("a { border-width: 2px * 3; }"), minify=True)
        self.assertEqual(output, "a{border-width:6px;}")

    def test_compile_from_file(self):
        """
        It can compile input from a file object
        """

        import tempfile
        in_file = tempfile.NamedTemporaryFile(mode='w+')
        in_file.write("a { border-width: 2px * 3; }")
        in_file.seek(0)
        output = compile(in_file, minify=True)
        self.assertEqual(output, "a{border-width:6px;}")

    def test_raises_exception(self):
        """
        Test if a syntax error raises an exception
        """
        from lesscpy.exceptions import CompilationError

        def fail_func():
            compile(StringIO("a }"), minify=True)

        self.assertRaises(CompilationError, fail_func)
