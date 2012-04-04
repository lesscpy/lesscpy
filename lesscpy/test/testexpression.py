import unittest
if __name__ == '__main__':
    import bootstrap
from lesscpy.plib.expression import Expression

class TestExpression(unittest.TestCase):        
    def test_basic(self):
        for test in [
            ['0', '+', '0', '0'],
            ['2', '+', '2', '4'],
            ['2.0', '+', '2', '4.0'],
            ['2', '+', '2.0', '4.0'],
            ['2.0', '+', '2.0', '4.0'],
            [('2.0',), '+', '2.0', '4.0'],
            [('2.0',), '+', ('2.0',), '4.0'],
            ['0px', '+', '0', '0'],
            ['2px', '+', '2', '4px'],
            ['2.0px', '+', '2', '4.0px'],
            [('2px', ' '), '+', '2.0', '4.0px'],
            ['2.0px', '+', '2.0', '4.0px'],
                        ]:
            e = Expression(test[:3])
            self.assertEqual(test[3], e.parse(None), str(test))
            
    def test_neg(self):
        for test in [
            ['-0', '+', '0', '0'],
            ['-2', '+', '-2', '-4'],
            ['-2.0', '+', '-2', '-4.0'],
            ['-2', '+', '-2.0', '-4.0'],
            ['-2.0', '+', '-2.0', '-4.0'],
            ['-0', '-', '0', '0'],
            ['-2', '-', '-2', '0'],
            ['-2.0', '-', '2', '-4.0'],
            ['-2', '-', '-2.0', '0.0'],
            ['2.0', '-', '-2.0', '4.0'],
            ['-0px', '+', '0', '0'],
            ['-2px', '+', '-2', '-4px'],
            ['-2.0', '+', '-2px', '-4.0px'],
            ['-2em', '+', '-2.0', '-4.0em'],
            ['-2.0s', '+', '-2.0s', '-4.0s'],
        ]:
            e = Expression(test[:3])
            self.assertEqual(test[3], e.parse(None), str(test))
            
    def testeq(self):
        for test in [
            ['0', '=', '0', True],
        ]:
            e = Expression(test[:3])
            self.assertEqual(test[3], e.parse(None), test)
        
    def testinput(self):
        e = Expression(['1a', '+', '1b'])
        self.assertRaises(SyntaxError, e.parse, None)


if __name__ == '__main__':
    unittest.main()