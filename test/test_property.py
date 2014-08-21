"""
Tests for CSS property.
"""
from lesscpy.lessc.parser import LessParser
from test.core import IntegrationTestCase


class TestProperty(IntegrationTestCase):
    """
    Tests for parsing of properties.
    """

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

    def test_interpolated_property_dash(self):
        content = '-www-@{a}-@{bb}: 2px;'
        self.inputContent(content)

        self.assertToken('css_vendor_property', '-www-')
        self.assertToken('less_variable_interpolated', '@a')
        self.assertToken('-', '-')
        self.assertToken('less_variable_interpolated', '@bb')
        self.assertToken('t_colon', ':')

        result = self.formatContent(content)
        self.assertEqual('', result)

    def test_variable_interpolation_full(self):
        """
        A property can be fully substitute by a variable.
        """
        result = self.formatContent(
            """
            @property: color;

            .widget {
              @{property}: #0ee;
            }
            """)

        self.assertEqual('.widget {\n  color: #00eeee;\n}', result)

    def test_variable_interpolation_end_dash(self):
        """
        A property end can be substitute by a variable prefixed with dash.
        """
        result = self.formatContent(
            """
            @property: color;

            .widget {
              background-@{property}: #0ee;
            }
            """)

        self.assertEqual('.widget {\n  background-color: #00eeee;\n}', result)

    def test_variable_interpolation_end(self):
        """
        A property end can be substitute by a variable.
        """
        result = self.formatContent(
            """
            @property: -color;

            .widget {
              background@{property}: #0ee;
            }
            """)

        self.assertEqual('.widget {\n  background-color: #00eeee;\n}', result)

    def test_variable_interpolation_start(self):
        """
        A property start can be substitute by a variable.
        """
        result = self.formatContent(
            """
            @property: back;

            .widget {
              @{property}ground-color: #0ee;
            }
            """)
        self.assertEqual('.widget {\n  background-color: #00eeee;\n}', result)

    def test_variable_interpolation_start_dash(self):
        """
        A property start can be substitute by a variable.
        """
        result = self.formatContent(
            """
            @property: background;

            .widget {
              @{property}-color: #0ee;
            }
            """)
        self.assertEqual('.widget {\n  background-color: #00eeee;\n}', result)

    def test_variable_interpolation_dash_inside_(self):
        """
        An interpolated property can contain a dash between 2 varibles.
        """
        result = self.formatContent(
            """
            .whitespace { color : black ; }
            """)
        self.assertEqual('.whitespace {\n  color: black;\n}', result)


    def test_white_space_after_name(self):
        """
        It can handle white spaces after property name.
        """
        result = self.formatContent(
            """
            .whitespace { color : black ; }
            """)
        self.assertEqual('.whitespace {\n  color: black;\n}', result)
