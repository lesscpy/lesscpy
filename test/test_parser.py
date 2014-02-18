"""
Unit test for the parser.
"""
import unittest

from six import StringIO

from lesscpy.lessc.parser import LessParser


class TestLessParser(unittest.TestCase):
    """
    Unit tests for LessParser.
    """

    def setUp(self):
        self.parser = LessParser()

    def test_parse_stream(self):
        """
        It can parse input from a file stream.
        """
        stream = StringIO("""
            @nice-blue: #5B83AD;
            """)

        self.parser.parse(file=stream)

        # A single object is parser which is the expected variable.
        self.assertEqual(1, len(self.parser.result))
        # This is a stream without a name so it sets default name.
        self.assertEqual('(stream)', self.parser.target)
        variable = self.parser.result[0]
        self.assertEqual('@nice-blue', variable.name)
        self.assertEqual(['#5b83ad'], variable.value)
