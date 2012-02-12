import unittest
if __name__ == '__main__':
    import bootstrap
from lesscpy.lessc.scope import Scope

class TestScope(unittest.TestCase):
    def test_scope(self):
        s = Scope()
        self.assertRaises(IndexError, s.pop)
        s.push()
        s.pop()
        self.assertRaises(IndexError, s.pop)
        self.assertRaises(IndexError, s.variables, '@var')

if __name__ == '__main__':
    unittest.main()