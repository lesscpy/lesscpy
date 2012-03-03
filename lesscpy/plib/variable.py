"""
"""
from .node import Node
class Variable(Node):
    def parse(self, scope):
        """
        """
        self.name = self.tokens.pop(0)
        self.value = self.tokens[1]
        return self
        
