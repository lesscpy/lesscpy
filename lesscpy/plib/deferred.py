# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.deferred
    :synopsis: Deferred mixin call.
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Jóhann T. Maríusson <jtm@robot.is>
"""
from .node import Node

class Deferred(Node):
    def __init__(self, mixin, args, lineno=0):
        """This node represents mixin calls 
        within the body of other mixins. The calls
        to these mixins are deferred until the parent
        mixin is called.
        args:
            mixin (Mixin): Mixin object
            args (list): Call arguments
        """
        self.mixin = mixin
        self.args = args
        self.lineno = lineno
    
    def parse(self, scope, error=False):
        """ Parse function.
        args:
            scope (Scope): Current scope
        returns:
            mixed
        """
        if hasattr(self.mixin, 'call'):
            return self.mixin.call(scope, self.args)
        mixins = scope.mixins(self.mixin.raw())
        if mixins:
            for mixin in mixins:
                res = mixin.call(scope, self.args)
                if res: return res
        else: 
            res = self
        if error:
            raise SyntaxError('NameError `%s`' % self.mixin.raw(True))
        return res
    
    def fmt(self, fills):
        """
        """
        return ''
    
    
