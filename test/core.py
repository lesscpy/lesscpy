"""
    Test bootstrap module. For flexible testing.
"""
import os
import glob
import unittest

import six

from lesscpy.lessc import formatter
from lesscpy.lessc.lexer import LessLexer
from lesscpy.lessc.parser import LessParser
from lesscpy.plib.block import Block
from lesscpy.plib.variable import Variable
from lesscpy.plib.statement import Statement


class Opt(object):
    def __init__(self):
        self.minify = False
        self.xminify = False
        self.tabs = True


def find_and_load_cases(cls, less_dir, css_dir, less_files=None, css_minimized=True):
    _less_path = os.path.join(os.path.dirname(__file__), less_dir)
    _css_path = os.path.join(os.path.dirname(__file__), css_dir)

    if less_files:
        LESS = [os.path.join(_less_path, "%s.less" % f) for f in less_files]
    else:
        LESS = glob.glob(os.path.join(_less_path, '*.less'))
    for less in LESS:
        lessf = less.split('.')[0].split('/')[-1]
        css = os.path.join(_css_path, lessf + '.css')
        if css_minimized:
            mincss = os.path.join(_css_path, lessf + '.min.css')
            test_method = create_case((less, css, mincss))
        else:
            test_method = create_case((less, css, None))
        test_method.__name__ = 'test_%s' % "_".join(reversed(os.path.basename(less).split('.')))
        setattr(cls, test_method.__name__, test_method)


def create_case(args):

    def assert_line(self, expect, result, file, line_no):
        """
        Check that lines are equal, showing a pretty diff.
        """
        diff_expect = expect.replace('\t', '\\t')
        diff_result = result.replace('\t', '\\t')
        self.assertEqual(
            expect,result,
            '\nExpecting\n%s\nGot\n%s\nFor %s: Line %d' % (
                diff_expect, diff_result, file, line_no))

    def do_case_expected(self):
        lessf, cssf, minf = args
        if os.path.exists(cssf):
            p = LessParser()
            p.parse(filename=lessf)
            f = formatter.Formatter(Opt())
            pout = f.format(p.result).split('\n')
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
                    assert_line(self, line, pout[i], cssf, i + 1)
                    i += 1
            if pl > i and i:
                self.fail(
                    "%s: result has more lines (%d > %d)" % (cssf, i, pl))
        else:
            self.fail("%s not found..." % cssf)
        if minf:
            if os.path.exists(minf):
                p = LessParser()
                opt = Opt()
                opt.minify = True
                p.parse(filename=lessf)
                f = formatter.Formatter(opt)
                mout = f.format(p.result).split('\n')
                ml = len(mout)
                i = 0
                with open(minf) as cssf:
                    for line in cssf.readlines():
                        if i >= ml:
                            self.fail(
                                "%s: result has less lines (%d < %d)" % (minf, i, ml))
                        assert_line(self, line.rstrip(), mout[i], cssf, i + 1)
                        i += 1
                if ml > i and i:
                    self.fail(
                        "%s: result has more lines (%d > %d)" % (minf, i, ml))
            else:
                self.fail("%s not found..." % minf)
    return do_case_expected


class ListReporter(object):
    """
    A reporter which accumulates errors in a list.
    """
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, filename, line_no, value):
        self.errors.append({
            'filename': filename,
            'line_no': line_no,
            'value': value,
            })

    def warning(self, filename, line_no, value):
        self.warnings.append({
            'filename': filename,
            'line_no': line_no,
            'value': value,
            })


class IntegrationTestCase(unittest.TestCase):
    """
    Generic test case for writing integration tests.
    """

    def assertIsVariable(self, node, name, value):
        """
        Check that `node` is a variable with `name` and `value`.
        """
        self.assertIsInstance(node, Variable)

        message = '\nExp %s:%s\nGot %s:%s' % (
            name, value, node.name, node.value)

        self.assertEqual(name, node.name, message)
        self.assertEqual(value, node.value, message)

    def assertIsBlock(self, node):
        """
        Check that node is a block.
        """
        self.assertIsInstance(node, Block)

    def assertIsStatement(self, node):
        """
        Check that node is a statement.
        """
        self.assertIsInstance(node, Statement)

    def assertNoErrors(self, reporter):
        """
        Check that reporter does not contains errors or warnings.
        """
        if reporter.errors:
            self.fail('Errors during parsing.\n%s' % (reporter.errors))

        if reporter.warnings:
            self.fail('Warnings during parsing.\n%s' % (reporter.warnings))

    def makeParser(self):
        """
        Return a new intance of parser.
        """
        error_reporter = ListReporter()
        return LessParser(error_reporter=error_reporter)

    def parseContent(self, content, parser=None):
        """
        Return the parsed elements for `content`.
        """
        if not parser:
            parser = self.makeParser()
        parser.parse(file=six.StringIO(content))
        self.assertNoErrors(parser.error_reporter)
        return parser.result

    def formatContent(self, content, parser=None):
        """
        Return the serialized CSS for LESS `content`.
        """
        new_formatter = formatter.Formatter()
        return new_formatter.format(self.parseContent(content, parser))

    def assertParsedResult(self, content, expected):
        """
        Check that content is parsed as expected.

        Expected should be passed as a indented multi-line string.

        The checks are done as a list to have a better diff.
        """
        result = self.formatContent(content)

        # Break multi-line in lines and remove start and end lines.
        expected_content = expected.split('\n')[1:-1]
        first_line = expected_content[0]
        padding = len(first_line) - len(first_line.lstrip(' '))
        expected_content = [line[padding:] for line in expected_content]

        self.assertEqual(expected_content, result.split('\n'))

    def inputContent(self, content):
        """
        Input content into the lexer.
        """
        self.lexer = LessLexer()
        self.lexer.input(six.StringIO(content))

    def assertToken(self, type, value):
        """
        Check that next token is of type and value.
        """
        token = self.lexer.token()
        message = '\nExp %s:%s\nGot %s:%s' % (
            type, value, token.type, token.value)
        self.assertEqual(token.type, type, message)
        self.assertEqual(token.value, value, message)
