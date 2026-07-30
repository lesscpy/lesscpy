"""
Test bootstrap module. For flexible testing.
"""

import glob
import os

from lesscpy.lessc import formatter, parser


class Opt:
    def __init__(self):
        self.minify = False
        self.xminify = False
        self.tabs = True


def find_and_load_cases(cls, less_dir, css_dir, less_files=None, css_minimized=True):
    _less_path = os.path.join(os.path.dirname(__file__), less_dir)
    _css_path = os.path.join(os.path.dirname(__file__), css_dir)

    if less_files:
        LESS = [os.path.join(_less_path, f"{f}.less") for f in less_files]
    else:
        LESS = glob.glob(os.path.join(_less_path, "*.less"))
    for less in LESS:
        lessf = less.rpartition(".")[0].split("/")[-1]
        css = os.path.join(_css_path, lessf + ".css")
        if css_minimized:
            mincss = os.path.join(_css_path, lessf + ".min.css")
            test_method = create_case((less, css, mincss))
        else:
            test_method = create_case((less, css, None))
        test_method.__name__ = "test_{}".format(
            "_".join(reversed(os.path.basename(less).split(".")))
        )
        setattr(cls, test_method.__name__, test_method)


def create_case(args):
    def do_case_expected(self):
        lessf, cssf, minf = args
        if os.path.exists(cssf):
            p = parser.LessParser()
            p.parse(filename=lessf)
            f = formatter.Formatter(Opt())
            pout = f.format(p).split("\n")
            pl = len(pout)
            i = 0
            with open(cssf) as cssf:
                for line in cssf:
                    if i >= pl:
                        self.fail(f"{cssf}: result has less lines ({i:d} < {pl:d})")
                    line = line.rstrip()
                    if not line:
                        continue
                    self.assertEqual(line, pout[i], f"{cssf}: Line {i + 1:d}")
                    i += 1
            if pl > i and i:
                self.fail(f"{cssf}: result has more lines ({i:d} > {pl:d})")
        else:
            self.fail(f"{cssf} not found...")
        if minf:
            if os.path.exists(minf):
                p = parser.LessParser()
                opt = Opt()
                opt.minify = True
                p.parse(filename=lessf)
                f = formatter.Formatter(opt)
                mout = f.format(p).split("\n")
                ml = len(mout)
                i = 0
                with open(minf) as cssf:
                    for line in cssf:
                        if i >= ml:
                            self.fail(f"{minf}: result has less lines ({i:d} < {ml:d})")
                        self.assertEqual(
                            line.rstrip(), mout[i], f"{minf}: Line {i + 1:d}"
                        )
                        i += 1
                if ml > i and i:
                    self.fail(f"{minf}: result has more lines ({i:d} > {ml:d})")
            else:
                self.fail(f"{minf} not found...")

    return do_case_expected
