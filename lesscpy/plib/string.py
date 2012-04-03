# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.string
    :synopsis: Less interpolated string node.
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Jóhann T. Maríusson <jtm@robot.is>
"""
import re
from .node import Node
from lesscpy.lessc import utility

class String(Node):
    def parse(self, scope):
        """Parse node
        args:
            scope (Scope): current scope
        raises:
            SyntaxError
        returns:
            str
        """
        self.scope = scope
        return re.sub(r'@\{([^\}]+)\}', lambda m: self.swap(m.group(1)), self.tokens)
    
    def swap(self, var):
        """ Replace variable
        args:
            var (str): variable
        raises:
            SyntaxError
        returns:
            str
        """
        var = self.scope.swap('@' + var)
        var = ''.join(utility.flatten(var))
        return var.strip("\"'")
    