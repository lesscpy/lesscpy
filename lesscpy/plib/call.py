"""
"""
from .node import Node
import lesscpy.lessc.utility as utility
class Call(Node):
    def parse(self, scope):
        self.parsed = [p.parse(scope) 
                       if hasattr(p, 'parse')
                       else p
                       for p in utility.flatten(self.tokens)]
        return self
    
    def format(self, fills):
        return ''.join([p.format(fills) 
                        if hasattr(p, 'format')
                        else p
                        for p in self.parsed])