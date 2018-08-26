import unittest

from lesscpy.lessc.scope import Scope
from lesscpy.plib.identifier import Identifier


class TestIdentifier(unittest.TestCase):
    def test_basic(self):
        fl = {'ws': ' ', 'nl': '\n'}
        for i in [
            ([], ''),
            (['.scope', ' ', 'a'], '.scope a'),
            (['a', ' ', '.scope'], 'a .scope'),
            (['a', '.scope'], 'a.scope'),
            (['a', '>', 'p', '>', 'h2'], 'a > p > h2'),
            (['a', '~', 'p', '+', 'h2'], 'a ~ p + h2'),
            (['*', 'html'], '* html'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(None).fmt(fl), r, i)

    def test_scope(self):
        fl = {'ws': ' ', 'nl': '\n'}
        sc = Scope()
        sc.push()
        sc.current = Identifier(['.current'], 0).parse(sc)
        for i in [
            (['.scope', ' ', 'a'], '.current .scope a'),
            (['a', ' ', '.scope'], '.current a .scope'),
            (['a', '.scope'], '.current a.scope'),
            (['a', '>', 'p', '>', 'h2'], '.current a > p > h2'),
            (['a', '~', 'p', '+', 'h2'], '.current a ~ p + h2'),
            (['>', 'p', '+', 'h2'], '.current > p + h2'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(sc).fmt(fl), r, i)

    def test_combinators(self):
        fl = {'ws': ' ', 'nl': '\n'}
        sc = Scope()
        sc.push()
        sc.current = Identifier(['.current'], 0).parse(sc)
        for i in [
            (['&', '.scope', ' ', 'a'], '.current.scope a'),
            (['.scope', '&', ' ', 'a'], '.scope.current a'),
            (['.scope', ' ', 'a', '&'], '.scope a.current'),
            (['&', '>', '.scope', ' ', 'a'], '.current > .scope a'),
            (['.span', '&', '.scope', ' ', 'a', '&'],
             '.span.current.scope a.current'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(sc).fmt(fl), r, i)
        sc.push()
        sc.current = Identifier(['&', '.next'], 0).parse(sc)
        id = Identifier(['&', '.top'], 0)
        self.assertEqual(id.parse(sc).fmt(fl), '.current.next.top')

    def test_groups(self):
        fl = {'ws': ' ', 'nl': '\n'}
        sc = Scope()
        sc.push()
        sc.current = Identifier(['.a', ',', '.b'], 0).parse(sc)
        for i in [
            (['&', '.scope', ' ', 'a'], '.a.scope a,\n.b.scope a'),
            (['.scope', '&', ' ', 'a'], '.scope.a a,\n.scope.b a'),
            (['.scope', ' ', 'a', '&'], '.scope a.a,\n.scope a.b'),
            (['>', '&', '.scope', ' ', 'a'], ' > .a.scope a,\n > .b.scope a'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(sc).fmt(fl), r, i)
        sc.current = Identifier(['.next'], 0).parse(sc)
        sc.push()
        sc.current = Identifier(['.c', ',', '.d'], 0).parse(sc)
        id = Identifier(['.deep'], 0)
        self.assertEqual(
            id.parse(sc).fmt(fl), '.a .next .c .deep,\n'
            '.b .next .c .deep,\n'
            '.a .next .d .deep,\n'
            '.b .next .d .deep')
        self.assertEqual(
            id.raw(), '.a% %.next% %.c% %.deep%'
            '.b% %.next% %.c% %.deep%'
            '.a% %.next% %.d% %.deep%'
            '.b% %.next% %.d% %.deep')

    def test_media(self):
        fl = {'ws': ' ', 'nl': '\n'}
        sc = Scope()
        sc.push()
        sc.current = Identifier(['@media', ' ', 'screen', ',', 'projection'],
                                0).parse(sc)
        self.assertEqual(sc.current.fmt(fl), '@media screen,projection')
        for i in [
            (['html'], 'html'),
        ]:
            t, r = i
            id = Identifier(t, 0)
            self.assertEqual(id.parse(sc).fmt(fl), r, i)
