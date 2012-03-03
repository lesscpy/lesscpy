"""
"""
from .node import Node
from lesscpy.lessc import utility

class Statement(Node):
    def parse(self, scope):
        """
        """
        self.parsed = list(utility.flatten(self.tokens))
        if self.parsed[0] == '@import':
            if len(self.parsed) > 4:
                # Media @import
                self.parsed.insert(3, ' ')
    
    def fmt(self, fills):
        """
        """
        return ''.join(self.parsed) + fills['eb']