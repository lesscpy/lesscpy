# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.deferred
    :synopsis: Deferred mixin call.
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Jóhann T. Maríusson <jtm@robot.is>
"""
from .node import Node
from lesscpy.lessc import utility

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
        self.tokens = [mixin, args]
        self.lineno = lineno
    
    def parse(self, scope, error=False):
        """ Parse function.
        args:
            scope (Scope): Current scope
        returns:
            mixed
        """
        res = False
        ident, args = self.tokens
#        if hasattr(mixin, 'call'):
#            return mixin.call(scope, args)
        ident.parse(scope)
        mixins = scope.mixins(ident.raw())
        if not mixins:
            ident.parse(None)
            mixins = scope.mixins(ident.raw())
        if not mixins:
            if scope.deferred:
                scope.current = scope.deferred
                ident.parse(scope)
                mixins = scope.mixins(ident.raw())
                scope.current = None
        if mixins:
            for mixin in mixins:
                res = mixin.call(scope, args)
                if res: break
            if res:
                scope.deferred = ident
                res = [p.parse(scope) for p in res if p]
                while(any(t for t in res if type(t) is Deferred)):
                    res = [p.parse(scope) for p in res if p]
                scope.deferred = None
        if error and not res:
            raise SyntaxError('NameError `%s`' % mixin.raw(True))
        return res
    
    
