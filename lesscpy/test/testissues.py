"""
    lesscpy tests. Issues
"""
import unittest
import os
import glob
import sys
import filecmp
sys.path.append('..')
from lessc import parser
from lessc import formatter

class TestCase(unittest.TestCase):
    pass

def create_test (pair):
    def do_test_expected(self):
        if os.path.exists(pair[1]):
            p = parser.LessParser()
            p.parse(filename=pair[0])
            f = formatter.Formatter()
            pout = f.format(p).split('\n')
            i = 0
            with open(pair[1]) as cssf:
                for line in cssf.readlines():
                    self.assertEqual(line.rstrip(), pout[i], '%s: Line %d' % (pair[1], i+1))
                    i += 1
        else: self.fail('%s not found' % pair[1])
    return do_test_expected

LESS = glob.glob( os.path.join('less/issues/', '*.less'))
for less in LESS:
    css = less.split('.')[0].split('/')[-1]
    css = 'css/issues/' + css + '.css'
    test_method = create_test((less, css))
    test_method.__name__ = 'test_%s' % less.replace('./-', '_')
    setattr(TestCase, test_method.__name__, test_method)

if __name__=="__main__":
    unittest.main()