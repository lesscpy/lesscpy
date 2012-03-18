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
        arguments = args if args else None
        if self.args:
            parsed = [v.parse(scope) 
                      if hasattr(v, 'parse') else v
                      for v in copy.deepcopy(self.args)]
            args = args if type(args) is list else [args]
            vars = [self._parse_arg(var, arg, scope) 
                    for arg, var in itertools.zip_longest([a for a in args if a != ','], parsed)]
            for var in vars:
                if var: scope.add_variable(var)
            if not arguments:
                arguments = [v.value for v in vars]
        if arguments:
            arguments = [' ' if a == ',' else a for a in arguments]
        else:
            arguments = ''
        scope.add_variable(Variable(['@arguments', 
                                     None, 
                                     arguments]).parse(scope))
        
    def _parse_arg(self, var, arg, scope):
        """
        """
        if type(var) is Variable:
            # kwarg
            if arg:
                if utility.is_variable(arg):
                    tmp = scope.variables(arg)
                    if not tmp: return None
                    var.value = tmp.value
                else:
                    var.value = arg
        else:
            #arg
            if utility.is_variable(var):
                if arg is None:
                    raise SyntaxError('Missing argument to mixin')
                elif utility.is_variable(arg):
                    tmp = scope.variables(arg)
                    if not tmp: return None
                    var = Variable([var, None, tmp.value]).parse(scope)
                else:
                    var = Variable([var, None, arg]).parse(scope)
            else:
                return None
        return var
    
    def call(self, scope, args=None):
        """
        """
        scope = copy.deepcopy(scope)
        body = copy.deepcopy(self.body)
        
        self.parse_args(args, scope)
        scope.update([self.scope], -1)
        
        body.parse(scope)
        r = list(utility.flatten([body.parsed, body.inner]))
        
        utility.rename(r, scope)
        return r
