import unittest
if __name__ == '__main__':
    import bootstrap
from lesscpy.lessc.scope import Scope
from lesscpy.plib.identifier import Identifier

class TestIdentifier(unittest.TestCase):    
    def test_basic(self):
        for i in [
            ([], ''),
            (['.scope', ' ', 'a'], '.scope a'),
            (['a', ' ', '.scope'], 'a .scope'),
            (['a', '.scope'], 'a.scope'),
            (['a', '>', 'p', '>', 'h2'], 'a> p> h2'),
            (['a', '~', 'p', '+', 'h2'], 'a~ p+ h2'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(None), r, i)
            
    def test_scope(self):
        sc = Scope()
        sc.push()
        sc.current = '.current'
        sc.push()
        sc.current = '.next'
        for i in [
            (['.scope', ' ', 'a'], '.current .scope a'),
            (['a', ' ', '.scope'], '.current a .scope'),
            (['a', '.scope'], '.current a.scope'),
            (['a', '>', 'p', '>', 'h2'], '.current a> p> h2'),
            (['a', '~', 'p', '+', 'h2'], '.current a~ p+ h2'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(sc), r, i)
            
    def test_combinators(self):
        sc = Scope()
        sc.push()
        sc.current = '.current'
        sc.push()
        sc.current = '.next'
        for i in [
            (['&.scope', ' ', 'a'], '.current.scope a'),
            (['.scope', '&', ' ', 'a'], '.scope.current a'),
            (['.scope', ' ', 'a', '&'], '.scope a.current'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(sc), r, i)

if __name__ == '__main__':
    unittest.main()
    