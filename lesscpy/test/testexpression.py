import unittest
if __name__ == '__main__':
    import bootstrap
from lesscpy.plib.expression import Expression

class TestExpression(unittest.TestCase):        
    def test_basic(self):
        for test in [
            ['0', '+', '0', 0],
            ['2', '+', '2', 4],
            ['2.0', '+', '2', 4.0],
            ['2', '+', '2.0', 4.0],
            ['2.0', '+', '2.0', 4.0],
            [('2.0',), '+', '2.0', 4.0],
            [('2.0',), '+', ('2.0',), 4.0],
            ['0px', '+', '0', 0],
            ['2px', '+', '2', '4px'],
            ['2.0px', '+', '2', '4.0px'],
            [('2px', ' '), '+', '2.0', '4.0px'],
            ['2.0px', '+', '2.0', '4.0px'],
                        ]:
            e = Expression(test[:3])
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
            e = Expression(test[:3])
            self.assertEqual(test[3], e.parse(None), str(test))
            
    def testnest(self):
        e = Expression(['2', '-', '-2'])
        f = Expression([['-', e], '*', '-3'])
        self.assertEqual(f.parse(None), 12)
        g = Expression(['2', '*', ['-', f]])
        self.assertEqual(g.parse(None), -24)
        h = Expression(['34', '-', ['-', g]])
        self.assertEqual(h.parse(None), 10)
        i = Expression([f, '-', h])
        self.assertEqual(i.parse(None), 2)
            
    def testdiv(self):
        e = Expression(['1', '/', '3'])
            
    def testinput(self):
        e = Expression(['1a', '+', '1b'])
        self.assertRaises(SyntaxError, e.parse, None)


if __name__ == '__main__':
    unittest.main()