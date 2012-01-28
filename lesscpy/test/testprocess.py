import unittest
from lesscpy.plib.process import Process
from lesscpy.plib.variable import Variable
from mockp import Mockp

class TestProcess(unittest.TestCase):
    def testswap(self):
        p = Process(Mockp([]))
        p.scope = [{}]
        self.assertRaises(SyntaxError, p.swap, '@var')
        p.scope = [{'@var': Variable(Mockp(['@var', ':', ['1']]))}]
        self.assertEqual('1', p.swap('@var'))
        p.scope.append({'@var': Variable(Mockp(['@var', ':', ['2']]))})
        self.assertEqual('2', p.swap('@var'))
        p.scope.pop()
        self.assertEqual('1', p.swap('@var'))
        self.assertEqual('1 ', p.swap('@var '))
        self.assertEqual('-1', p.swap('-@var'))
        self.assertEqual('-1 ', p.swap('-@var '))
        
    def testswapvarvar(self):
        p = Process(Mockp([]))
        p.scope = [{'@var': Variable(Mockp(['@var', ':', ['1']]))}]
        p.scope.append({'@name': Variable(Mockp(['@name', ':', ['var']]))})
        self.assertEqual('1', p.swap('@@name'))
        self.assertEqual('1 ', p.swap('@@name '))
        self.assertEqual('-1', p.swap('-@@name'))
        self.assertEqual('-1 ', p.swap('-@@name '))
    
    def testreplace(self):
        p = Process(Mockp([]))
        p.scope = [{'@var': Variable(Mockp(['@var', ':', ['1']]))}]
        p.scope.append({'@var2': Variable(Mockp(['@var2', ':', ['2']]))})
        t = p.replace_vars(['1', '@var2', 'm', '@var'])
        self.assertEqual(t, ['1', '2', 'm', '1'])
        t = p.replace_vars(['1', '-@var2 ', 'm', '-@var'])
        self.assertEqual(t, ['1', '-2 ', 'm', '-1'])
    
if __name__ == '__main__':
    unittest.main()