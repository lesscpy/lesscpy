"""
Unit tests for the lexer.
"""
from tempfile import NamedTemporaryFile
import unittest

from six import StringIO

from lesscpy.lessc.lexer import LessLexer


class TestLessLexer(unittest.TestCase):
    """
    Unit tests for LessLexer
    """

    def setUp(self):
        self.lexer = LessLexer()

    def inputContent(self, content):
        """
        Input content into the lexer.
        """
        self.lexer.input(StringIO(content))

    def assertToken(self, type, value):
        """
        Check that next token is of type and value.
        """
        token = self.lexer.token()
        self.assertEqual(token.type, type)
        self.assertEqual(token.value, value)

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

    def test_interpolated_property_full(self):
        self.inputContent('@{var}: black;')

        self.assertToken('less_variable_interpolated', '@var')
        self.assertToken('t_colon', ':')

    def test_interpolated_property_css_vendor(self):
        self.inputContent('@{var}-color: black;')

        self.assertToken('less_variable_interpolated', '@var')
        self.assertToken('css_vendor_property', '-color')
        self.assertToken('t_colon', ':')


    def test_interpolated_property_css_vendor(self):
        self.inputContent('@{var}color: black;')

        self.assertToken('less_variable_interpolated', '@var')
        self.assertToken('css_property', 'color')
        self.assertToken('t_colon', ':')
