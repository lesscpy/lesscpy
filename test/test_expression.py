"""
    lesscpy expression tests.
"""
import unittest

from lesscpy.plib.expression import Expression


class TestExpression(unittest.TestCase):
    def test_basic(self):
        for test in [
            ['0', '+', '0', '0'],
            ['2', '+', '2', '4'],
            ['2.0', '+', '2', '4'],
            ['2', '+', '2.0', '4'],
            ['2.0', '+', '2.0', '4'],
            [('2.0', ), '+', '2.0', '4'],
            [('2.0', ), '+', ('2.0', ), '4'],
            ['0px', '+', '0', '0'],
            ['2px', '+', '2', '4px'],
            ['2.0px', '+', '2', '4px'],
            [('2px', ' '), '+', '2.0', '4px'],
            ['2.0px', '+', '2.0', '4px'],
        ]:
            e = Expression(test[:3])
            self.assertEqual(test[3], e.parse(None), str(test))

    def test_neg(self):
        for test in [
            ['-0', '+', '0', '0'],
            ['-2', '+', '-2', '-4'],
            ['-2.0', '+', '-2', '-4'],
            ['-2', '+', '-2.0', '-4'],
            ['-2.0', '+', '-2.0', '-4'],
            ['-0', '-', '0', '0'],
            ['-2', '-', '-2', '0'],
            ['-2.0', '-', '2', '-4'],
            ['-2', '-', '-2.0', '0'],
            ['2.0', '-', '-2.0', '4'],
            ['-0px', '+', '0', '0'],
            ['-2px', '+', '-2', '-4px'],
            ['-2.0', '+', '-2px', '-4px'],
            ['-2em', '+', '-2.0', '-4em'],
            ['-2.0s', '+', '-2.0s', '-4s'],
        ]:
            e = Expression(test[:3])
            self.assertEqual(test[3], e.parse(None), str(test))

    def test_op(self):
        for test in [
            ['0', '=', '0', True],
            ['1', '>', '2', False],
            ['1', '<', '2', True],
            ['1', '>=', '2', False],
            ['1', '=<', '2', True],
        ]:
            e = Expression(test[:3])
            self.assertEqual(test[3], e.parse(None), test)
