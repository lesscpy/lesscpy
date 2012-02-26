"""
"""
from .node import Node
import lesscpy.lessc.utility as utility
class Call(Node):
    def parse(self, scope):
        parsed = self.process(self.tokens, scope)
        return ''.join([p for p in parsed])
