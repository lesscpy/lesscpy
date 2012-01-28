import unittest
from lesscpy.plib.expression import Expression
from mockp import Mockp

class TestExpression(unittest.TestCase):        
    def test_basic(self):
        for test in [
            ['0', '+', '0', 0],
            ['2', '+', '2', 4],
            ['2.0', '+', '2', 4.0],
            ['2', '+', '2.0', 4.0],
            ['2.0', '+', '2.0', 4.0],
                        ]:
            e = Expression(Mockp(test[:3]))
            self.assertEqual(test[3], e.parse(None), str(test))
            
    def test_neg(self):
        for test in [
            ['-0', '+', '0', 0],
            ['-2', '+', '-2', -4],
            ['-2.0', '+', '-2', -4.0],
            ['-2', '+', '-2.0', -4.0],
            ['-2.0', '+', '-2.0', -4.0],
            ['-0', '-', '0', 0],
            ['-2', '-', '-2', 0],
            ['-2.0', '-', '2', -4.0],
            ['-2', '-', '-2.0', 0],
            ['2.0', '-', '-2.0', 4.0],
            ['-0px', '+', '0', 0],
            ['-2px', '+', '-2', '-4px'],
            ['-2.0', '+', '-2px', '-4.0px'],
            ['-2em', '+', '-2.0', '-4.0em'],
            ['-2.0s', '+', '-2.0s', '-4.0s'],
                        ]:
            e = Expression(Mockp(test[:3]))
            self.assertEqual(test[3], e.parse(None), str(test))
            
    def testnest(self):
        e = Expression(Mockp(['2', '-', '-2']))
        f = Expression(Mockp([['-', e], '*', '-3']))
        self.assertEqual(f.parse(None), 12)
        g = Expression(Mockp(['2', '*', ['-', f]]))
        self.assertEqual(g.parse(None), -24)
        h = Expression(Mockp(['34', '-', ['-', g]]))
        self.assertEqual(h.parse(None), 10)
        i = Expression(Mockp([f, '-', h]))
        self.assertEqual(i.parse(None), 2)
            
    def testdiv(self):
        e = Expression(Mockp(['1', '/', '3']))
            
    def testinput(self):
        e = Expression(Mockp(['1a', '+', '1b']))
        self.assertRaises(SyntaxError, e.parse, None)


if __name__ == '__main__':
    unittest.main()