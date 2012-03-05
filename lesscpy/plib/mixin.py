"""
    
"""
import copy
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
    
    def parse_args(self, args):
        """
        """
        if self.args:
            parsed = [v.parse(None) 
                      if hasattr(v, 'parse') else v
                      for v in copy.deepcopy(self.args)]
            if args:
                l = len(args)
                for i in range(len(parsed)):
                    if i < l and args[i]:
                        if utility.is_variable(args[i]):
                            pass
                        elif type(parsed[i]) is Variable: 
                            parsed[i].value = args[i]
                        else:
                            parsed[i] = Variable([parsed[i], 
                                                  None, 
                                                  args[i]]).parse(None)
            return parsed
        return []
    
    def call(self, scope, args=None):
        """
        """
        if args:
            args = [a for a in args if a != ',']
        scope = copy.deepcopy(scope)
        body = copy.deepcopy(self.body)
        for v in self.parse_args(args):
            if type(v) is Variable:
                scope.add_variable(v) 
        scope.update([self.scope], -1)
        return body.parse(scope).copy(scope)
