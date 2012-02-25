"""
"""
from .node import Node
class Variable(Node):
    def parse(self, scope):
        """
        """
        self.name = self.tokens.pop(0)