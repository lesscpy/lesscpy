"""
Unit tests for the lexer.
"""
from tempfile import NamedTemporaryFile
import unittest

from six import StringIO

from lesscpy.lessc.lexer import LessLexer


class TestLessLexer(unittest.TestCase):
    """
    Tests for general LessLexer methods.

    Tests for token method are split into dedicated tests for each node type.
    """

    def setUp(self):
        self.lexer = LessLexer()

    def test_input_stream(self):
        """
        It can load content from a string.
        """
        file = StringIO("""
            @simple-var: 1;
            """)

        self.lexer.input(file)

        token = self.lexer.token()
        self.assertEqual('@simple-var', token.value)

    def test_input_path(self):
        """
        It can load content from a path.
        """
        file = NamedTemporaryFile()
        file.write(b"""
            @simple-var: 1;
            """)
        file.seek(0)

        self.lexer.input(file.name)

        token = self.lexer.token()
        self.assertEqual('@simple-var', token.value)
