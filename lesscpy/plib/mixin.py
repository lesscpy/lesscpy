"""
    
"""
import copy, itertools
from .node import Node
from .block import Block
from .variable import Variable
from lesscpy.lessc import utility

class Mixin(Node):
    def parse(self, scope):
        """
        """
        self.name, args = self.tokens[0]
        self.args = [a for a in args if a != ','] if args else []
        self.body = Block([None, self.tokens[1]], 0)
        self.scope = copy.deepcopy(scope[-1])
        return self
    
    def parse_args(self, args, scope):
        """
        """
        if self.args:
            parsed = [v.parse(scope) 
                      if hasattr(v, 'parse') else v
                      for v in copy.deepcopy(self.args)]
            args = args if type(args) is list else [args]
            for arg, var in itertools.zip_longest(args, parsed):
                if type(var) is Variable and arg: 
                    var.value = arg
                elif utility.is_variable(arg):
                    tmp = scope.variables(arg)
                    if not tmp: continue
                    var = Variable([var, None, tmp.name]).parse(scope)
                elif utility.is_variable(var):
                    var = Variable([var, None, arg]).parse(scope)
                scope.add_variable(var)
    
    def call(self, scope, args=None):
        """
        """
        if args:
            args = [a for a in args if a != ',']
        scope = copy.deepcopy(scope)
        body = copy.deepcopy(self.body)
        self.parse_args(args, scope)
        scope.update([self.scope], -1)
        return body.parse(scope).copy(scope)
