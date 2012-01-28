"""
    Parametered Mixin Node.
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
from collections import deque
import lesscpy.lessc.utility as utility
import copy
from .process import Process
from .node import Node

class Mixin(Process):
    """ Mixin Node.
    """
    def parse(self, scope, stash=None):
        """ Parse Node
            @param list: current scope
        """
        self.stash = stash
        self.name = self._p[1][0]
        if len(self._p[1]) > 1:
            if type(self._p[1][2]) is list:
                self.argv = [[u[0], u[2]] if type(u) is list
                             else [u, None]
                             for u in self._p[1][2]
                             if u and u != ',']
            else:
                self.argv = self._p[1][2]
            self.argc = len(self.argv)
        else:
            self.argv = []
            self.argc = 0
        self.prop = self._p[2]
    
    def call(self, args, scope=[{}]):
        """ Call mixin function.
            @param list: Arguments passed to mixin
            @return: Property list
        """
        if self.argv == '@arguments':
            return [self.replace_arguments(copy.copy(p), args).parse(self.scope) 
                    for p in self.prop 
                    if p]
        self.scope = scope 
        self.scope[0].update(self.stash)  
        prop = [copy.copy(p) for p in self.prop if p]
        prop = utility.flatten([p.call(args, self.scope) 
                                if type(p) is Mixin else p 
                                for p in prop])
        self._process_args(args)
        return [p.parse(self.scope) for p in prop]
    
    def _process_args(self, args):
        """ Process arguments to mixin call.
            Handle the @arguments variable
            @param list: arguments
        """
        variables = []
        if args: 
            args = [a for a in self.process_tokens(args) 
                    if a != ',']
        else: 
            args = []
        args = deque(args)
        for v in self.argv:
            if args:
                u = args.popleft()
                variables.append((v[0], u))
            else:
                variables.append(v)
        for v in variables:
            self._create_variable(v)
        # Special @arguments
        arguments = [v[1] for v in variables]
        arguments.extend(args)
        self._create_variable(('@arguments', [arguments]))    
    
    def _create_variable(self, l):
        """ Create new variable in scope, from list or index
            @param tuple: name/value pair
        """
        assert(len(l) == 2)
        var = Node()
        var._name, var._value = l
        self.scope[0][var._name] = var
        
    def replace_arguments(self, p, args):
        """ Replace the special @arguments variable
            @param Property object: Property object
            @param list: Replacement list
            @return: Property object
        """
        p._p[3] = args
        return p
    
