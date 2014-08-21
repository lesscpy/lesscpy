"""
Tests for CSS import statement.
"""
import os

from lesscpy.lessc.parser import LessParser
from test.core import IntegrationTestCase


class TestImport(IntegrationTestCase):
    """
    Tests for token and parsing of selectors.
    """

    def setUp(self):
        super(TestImport, self).setUp()

    def makeMockedImportParser(self):
        """
        Return a parser with a mocked import method.
        """
        parser = self.makeParser()
        # We mock the low level import call as we only care parsed data.
        import_calls = []
        parser._parseImport = (
            lambda path, line_no: import_calls.append((path, line_no)))
        return (parser, import_calls)

    def test_interpolated_import(self):
        self.inputContent('@import "@{theme}.less";')

        self.assertToken('css_import', '@import')
        self.assertToken('t_ws', ' ')
        self.assertToken('t_isopen', '"')
        self.assertToken('less_variable_interpolated', '@theme')
        self.assertToken('css_string', '.less')
        self.assertToken('t_isclose', '"')
        self.assertToken('t_semicolon', ';')


    def test_normal(self):
        """
        It will call import for the specified path.
        """
        parser, import_calls = self.makeMockedImportParser()

        self.parseContent(
            """
            @import "some_value.less";
            """, parser=parser)

        self.assertEqual(
            [(os.path.abspath('some_value.less'), 2)], import_calls)

    def test_no_extension(self):
        """
        It will add .less as the file extension.
        """
        parser, import_calls = self.makeMockedImportParser()

        self.parseContent(
            """
            @import "some_value";
            """, parser=parser)

        self.assertEqual(
            [(os.path.abspath('some_value.less'), 2)], import_calls)

    def test_interpolation_import(self):
        """
        Variable interpolation can be used in imports.

        http://lesscss.org/features/#variables-feature-import-statements
        """
        parser, import_calls = self.makeMockedImportParser()

        self.parseContent(
            """
            @theme: "name";
            @import "@{theme}.less";
            """, parser=parser)

        self.assertEqual([(os.path.abspath('name.less'), 3)], import_calls)

    def test_css_statement(self):
        """
        Imports for css files will be kept unchanged as a normal statement.
        """
        parser, import_calls = self.makeMockedImportParser()

        result = self.formatContent(
            """
            @import    "name.css"   ;
            """, parser=parser)

        self.assertEqual([], import_calls)
        self.assertEqual('@import "name.css";', result)
