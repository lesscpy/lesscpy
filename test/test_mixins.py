"""
Implementation of mixins.

Documentation : http://lesscss.org/features/#mixins-feature
"""
from StringIO import StringIO
import unittest

from lesscpy.lessc.formatter import Formatter
from lesscpy.lessc.parser import LessParser


class TestMixins(unittest.TestCase):
    """
    Integration tests for Mixins.
    """

    def setUp(self):
        self.parser = LessParser()
        self.formatter = Formatter()

    def assertParsedResult(self, content, expected):
        """
        Check that content is parsed as expected.

        Expected should be passed as a indented multi-line string.

        The checks are done as a list to have a better diff.
        """
        self.parser.parse(filestream=StringIO(content))
        result = self.formatter.format(self.parser)
        # Break multi-line in lines and remove start and end lines.
        expected_content = expected.split('\n')[1:-1]
        first_line = expected_content[0]
        padding = len(first_line) - len(first_line.lstrip(' '))
        expected_content = [line[padding:] for line in expected_content]
        self.assertEqual(expected_content, result.split('\n'))


    def test_simple_mixin(self):
        """
        Mixins are a way of including ("mixing in") a bunch of properties
        from one rule-set into another rule-set.

        Example: http://lesscss.org/features/#features-overview-feature-mixins
        """
        self.assertParsedResult("""
            .bordered {
              border-top: dotted 1px black;
              border-bottom: solid 2px black;
            }

            #menu a {
              color: #111;
              .bordered;
            }

            .post a {
              color: red;
              .bordered;
            }
            """,
            """
            .bordered {
              border-top: dotted 1px black;
              border-bottom: solid 2px black;
            }
            #menu a {
              color: #111111;
              border-top: dotted 1px black;
              border-bottom: solid 2px black;
            }
            .post a {
              color: red;
              border-top: dotted 1px black;
              border-bottom: solid 2px black;
            }
            """
            )

    def test_class_and_id_selectors(self):
        """
        You can mix-in class selectors and id selectors.

        Example: http://lesscss.org/features/#mixins-feature
        """
        self.assertParsedResult("""
            .a, #b {
              color: red;
            }
            .mixin-class {
              .a();
            }
            .mixin-id {
              #b();
            }
            """,
            """
            .a,
            #b {
              color: red;
            }
            .mixin-class {
              color: red;
            }
            .mixin-id{
              color: red;
            }
            """
            )
