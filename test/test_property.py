"""
Tests for CSS property.
"""
from lesscpy.lessc.parser import LessParser
from lesscpy.plib.block import Block
from lesscpy.plib.variable import Variable
from test.core import IntegrationTestCase


class TestPropertyParsing(IntegrationTestCase):
    """
    Tests for parsing of properties.
    """

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

    def test_variable_interpolation_end(self):
        """
        A property end can be substitute by a variable.
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

    def test_variable_interpolation_start(self):
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

    def test_white_space_after_name(self):
        """
        """
        result = self.parseContent(
            """
            .whitespace { color : black ; }
            """)
        self.assertEqual(
            '.whitespace {color: black;}\n', result[0].fmt())
