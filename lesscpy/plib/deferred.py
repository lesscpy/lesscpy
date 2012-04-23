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
        """This node represents mixin calls. The calls
        to these mixins are deferred until the second 
        parse cycle.
        args:
            mixin (Mixin): Mixin object
            args (list): Call arguments
        """
        self.tokens = [mixin, args]
        self.lineno = lineno
    
    def parse(self, scope, error=False):
        """ Parse function. We search for mixins
        first within current scope then fallback
        to global scope. The special scope.deferred
        is used when local scope mixins are called 
        within parent mixins. 
        args:
            scope (Scope): Current scope
        returns:
            mixed
        """
        res = False
        ident, args = self.tokens
        ident.parse(scope)
        mixins = scope.mixins(ident.raw())
        
        if not mixins:
            ident.parse(None)
            mixins = scope.mixins(ident.raw())
            
            
        if not mixins:
            store = [t for t in scope.deferred.parsed[-1]]
            while scope.deferred.parsed[-1]:
                scope.current = scope.deferred
                ident.parse(scope)
                mixins = scope.mixins(ident.raw())
                scope.current = None
                if mixins:
                    break
                scope.deferred.parsed[-1].pop()
            scope.deferred.parsed[-1] = store
                
        if mixins:
            for mixin in mixins:
                res = mixin.call(scope, args)
                if res: break
            if res:
                scope.deferred = ident
                res = [p.parse(scope) for p in res if p]
                while(any(t for t in res if type(t) is Deferred)):
                    res = [p.parse(scope) for p in res if p]
                
        if error and not res:
            raise SyntaxError('NameError `%s`' % mixin.raw(True))
        return res
    
    
