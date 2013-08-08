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


def create_test(args):
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
                        self.fail(
                            "%s: result has less lines (%d < %d)" % (cssf, i, pl))
                    line = line.rstrip()
                    if not line:
                        continue
                    self.assertEqual(
                        line, pout[i], '%s: Line %d' % (cssf, i + 1))
                    i += 1
            if pl > i and i:
                self.fail(
                    "%s: result has more lines (%d > %d)" % (cssf, i, pl))
        else:
            self.fail("%s not found..." % cssf)
    return do_test_expected

LESS = glob.glob(os.path.join('less/issues', '*.less'))
_less_path = os.path.join(os.path.dirname(__file__), 'less', 'issues')
_css_path = os.path.join(os.path.dirname(__file__), 'css', 'issues')

LESS = glob.glob(os.path.join(_less_path, '*.less'))
for less in LESS:
    lessf = less.split('.')[0].split('/')[-1]
    css = os.path.join(_css_path, lessf + '.css')
    mincss = os.path.join(_css_path, lessf + '.min.css')
    test_method = create_test((less, css, mincss))
    test_method.__name__ = 'test_%s' % "_".join(reversed(os.path.basename(less).split('.')))
    setattr(TestCase, test_method.__name__, test_method)

if __name__ == "__main__":
    unittest.main()
