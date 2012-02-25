"""
"""
from .node import Node
from lesscpy.lessc import utility
class Identifier(Node):
    def parse(self, scope):
        """
        """
        if scope:
            scopename = [name for name in scope.scopename]
            scopename.extend(self.tokens)
        else:
            scopename = self.tokens
        return ''.join(utility.flatten(scopename)).strip()
