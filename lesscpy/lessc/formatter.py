# -*- coding: utf8 -*-
"""
.. module:: lesscpy.lessc.formatter
    :synopsis: CSS Formatter class.

    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Johann T. Mariusson <jtm@robot.is>
"""


class _DefaultArguments(object):
    """
    Default arguments for the formatter.
    """
    def __init__(self):
        self.xminify = False
        self.minify = False
        self.tabs = False
        self.spaces = 2

class Formatter(object):
    """
    See _DefaultArguments for available configuration options.
    """

    def __init__(self, args=None):
        if args is None:
            args = _DefaultArguments()
        self.args = args

    def format(self, results):
        """
        """
        if not results:
            return ''
        eb = '\n'
        if self.args.xminify:
            eb = ''
            self.args.minify = True
        self.items = {}
        if self.args.minify:
            self.items.update({
                'nl': '',
                'tab': '',
                'ws': '',
                'eb': eb
            })
        else:
            tab = '\t' if self.args.tabs else ' ' * int(self.args.spaces)
            self.items.update({
                'nl': '\n',
                'tab': tab,
                'ws': ' ',
                'eb': eb
            })
        self.out = [u.fmt(self.items)
                    for u in results
                    if u]
        return ''.join(self.out).strip()
