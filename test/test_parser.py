"""
Unit test for the parser.
"""
from StringIO import StringIO
import unittest

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

        self.parser.parse(filestream=stream)

        # A single object is parser which is the expected variable.
        self.assertEqual(1, len(self.parser.result))
        variable = self.parser.result[0]
        self.assertEqual('@nice-blue', variable.name)
        self.assertEqual(['#5b83ad'], variable.value)
