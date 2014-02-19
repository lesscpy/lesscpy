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

    def test_interpolated_property_css_vendor(self):
        self.inputContent('-www-@{a}-@{bb}: 2px;')

        self.assertToken('css_vendor_property', '-www-')
        self.assertToken('less_variable_interpolated', '@a')
        self.assertToken('-', '-')
        self.assertToken('less_variable_interpolated', '@bb')
        self.assertToken('t_colon', ':')

    def test_variable_interpolation_full(self):
        """
        A property can be fully substitute by a variable.
        """
        result = self.parseContent(
            """
            @property: color;

            .widget {
              @{property}: #0ee;
            }
            """)

        self.assertIsVariable(result[0], '@property', [('color',)])
        block = result[1]
        self.assertIsBlock(block)
        self.assertEqual(
            '.widget {color: #00eeee;}\n', block.fmt())

    def test_variable_interpolation_end_dash(self):
        """
        A property end can be substitute by a variable prefixed with dash.
        """
        result = self.parseContent(
            """
            @property: color;

            .widget {
              background-@{property}: #0ee;
            }
            """)

        self.assertIsVariable(result[0], '@property', [('color',)])
        block = result[1]
        self.assertIsBlock(block)
        self.assertEqual(
            '.widget {background-color: #00eeee;}\n', block.fmt())

    def test_variable_interpolation_end(self):
        """
        A property end can be substitute by a variable.
        """
        result = self.parseContent(
            """
            @property: -color;

            .widget {
              background@{property}: #0ee;
            }
            """)

        self.assertIsVariable(result[0], '@property', [('-color',)])
        block = result[1]
        self.assertIsBlock(block)
        self.assertEqual(
            '.widget {background-color: #00eeee;}\n', block.fmt())

    def test_variable_interpolation_start(self):
        """
        A property start can be substitute by a variable.
        """
        result = self.parseContent(
            """
            @property: back;

            .widget {
              @{property}ground-color: #0ee;
            }
            """)
        self.assertIsBlock(result[1])
        self.assertEqual(
            '.widget {background-color: #00eeee;}\n', result[1].fmt())

    def test_variable_interpolation_start_dash(self):
        """
        A property start can be substitute by a variable.
        """
        result = self.parseContent(
            """
            @property: background;

            .widget {
              @{property}-color: #0ee;
            }
            """)
        self.assertIsBlock(result[1])
        self.assertEqual(
            '.widget {background-color: #00eeee;}\n', result[1].fmt())

    def test_variable_interpolation_dash_inside_(self):
        """
        An interpolated property can contain a dash between 2 varibles.
        """
        result = self.parseContent(
            """
            .whitespace { color : black ; }
            """)
        self.assertEqual(
            '.whitespace {color: black;}\n', result[0].fmt())


    def test_white_space_after_name(self):
        """
        It can handle white spaces after property name.
        """
        result = self.parseContent(
            """
            .whitespace { color : black ; }
            """)
        self.assertEqual(
            '.whitespace {color: black;}\n', result[0].fmt())
