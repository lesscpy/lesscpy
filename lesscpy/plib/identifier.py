"""
"""
from .node import Node
from lesscpy.lessc import utility
class Identifier(Node):
    def parse(self, scope):
        """
        """
        return ''.join(utility.flatten(self.tokens)).strip()