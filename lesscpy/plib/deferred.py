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
    def __init__(self, mixin, args, lineno=0, caller=None):
        """This node represents mixin calls. The calls
        to these mixins are deferred until the second 
        parse cycle. lessc.js allows calls to mixins not 
        yet defined or known.
        args:
            mixin (Mixin): Mixin object
            args (list): Call arguments
        """
        self.tokens = [mixin, args]
        self.lineno = lineno
        self.caller = caller
    
    def parse(self, scope, error=False):
        """ Parse function. We search for mixins
        first within current scope then fallback
        to global scope. The special scope.deferred
        is used when local scope mixins are called 
        within parent mixins. 
        If nothing is found we fallback to block-mixin
        as lessc.js allows calls to blocks and mixins to
        be inter-changable.
        clx: This method is a HACK that stems from 
        poor design elsewhere. I will fix it 
        when I have more time.
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
            if scope.deferred:
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
    
        if not mixins:
            # Fallback to blocks
            block = scope.blocks(ident.raw())
            if not block:
                ident.parse(None)
                self.caller.parse(None)
                block = scope.blocks(ident.raw())
            if block:
                scope.current = self.caller
                res = block.copy_inner(scope)
                scope.current = None
                
        if mixins:
            for mixin in mixins:
                res = mixin.call(scope, args)
                if res: 
                    # Add variables to scope to support
                    # closures
                    [scope.add_variable(v) for v in mixin.vars]
                    scope.deferred = ident
                    break
                
        if res:
            res = [p.parse(scope) for p in res if p]
            while(any(t for t in res if type(t) is Deferred)):
                res = [p.parse(scope) for p in res if p]
                
        if error and not res:
            raise SyntaxError('NameError `%s`' % mixin.raw(True))
        return res
    
    def copy(self):
        """ Returns self (used when Block objects are copy'd)
        returns:
            self
        """
        return self
    
    
