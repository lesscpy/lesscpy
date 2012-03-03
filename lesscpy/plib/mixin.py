"""
    
"""
import copy
from .node import Node
from .block import Block
from .variable import Variable

class Mixin(Node):
    def parse(self, scope):
        """
        """
        self.name, self.args = self.tokens[0]
        self.body = Block([None, self.tokens[1]], 0)
        return self
    
    def parse_args(self, args):
        """
        """
        if self.args:
            parsed = [v.parse(None) 
                      if hasattr(v, 'parse') else v
                      for v in copy.deepcopy(self.args)]
            if args:
                for i in range(len(parsed)):
                    if args[i]:
                        if type(parsed[i]) is Variable: 
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
        scope = copy.deepcopy(scope)
        body = copy.deepcopy(self.body)
        for v in self.parse_args(args):
            scope.add_variable(v) 
        return body.parse(scope).copy(scope)
