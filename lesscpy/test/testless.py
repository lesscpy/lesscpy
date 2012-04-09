"""
    lesscpy tests.
"""
import unittest
import os
import glob
import bootstrap

from lesscpy.lessc import parser
from lesscpy.lessc import formatter

class TestCase(unittest.TestCase):
    pass

class Opt(object):
    def __init__(self):
        self.minify = False
        self.xminify = False
        self.tabs = True

def create_test (args):
    def do_test_expected(self):
        lessf, cssf, minf = args
        if os.path.exists(cssf):
            p = parser.LessParser()
            p.parse(filename=lessf)
            f = formatter.Formatter(Opt())
            pout = f.format(p).split('\n')
            pl = len(pout)
            i = 0
            with open(cssf) as cssf:
                for line in cssf.readlines():
                    if i >= pl:
                        self.fail("%s: result has less lines (%d < %d)" % (cssf, i, pl))
                    line = line.rstrip()
                    if not line: continue
                    self.assertEqual(line, pout[i], '%s: Line %d' % (cssf, i+1))
                    i += 1
            if pl > i and i:
                self.fail("%s: result has more lines (%d > %d)" % (cssf, i, pl))
        else:
            self.fail("%s not found..." % cssf)
        if os.path.exists(minf):
            p = parser.LessParser()
            opt = Opt()
            opt.minify = True
            p.parse(filename=lessf)
            f = formatter.Formatter(opt)
            mout = f.format(p).split('\n')
            ml = len(mout)
            i = 0
            with open(minf) as cssf:
                for line in cssf.readlines():
                    if i >= ml:
                        self.fail("%s: result has less lines (%d < %d)" % (minf, i, ml))
                    self.assertEqual(line.rstrip(), mout[i], '%s: Line %d' % (minf, i+1))
                    i += 1
            if ml > i and i:
                self.fail("%s: result has more lines (%d > %d)" % (minf, i, ml))
        else:
            self.fail("%s not found..." % minf)
    return do_test_expected

LESS = glob.glob( os.path.join('less/', '*.less'))
for less in LESS:
    lessf = less.split('.')[0].split('/')[-1]
    css = 'css/' + lessf + '.css'
    mincss = 'css/' + lessf + '.min.css'
    test_method = create_test((less, css, mincss))
    test_method.__name__ = 'test_%s' % less.replace('./-', '_')
    setattr(TestCase, test_method.__name__, test_method)

if __name__=="__main__":
    unittest.main()
