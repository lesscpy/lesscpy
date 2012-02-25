"""
"""
from .node import Node
from lesscpy.lessc import utility
class Property(Node):
    pass 

    def parse(self, scope):
        property, style = self.tokens
        self.property = property[0]
        self.parsed = []
        if style:
            self.parsed = [p.parse(scope) 
                           if hasattr(p, 'parse')
                           else p
                           for p in utility.flatten(style)]
            self.parsed = [p for p in self.parsed if p]
        return self
        
    def format(self, fills):
        """
        """
        f = "%(tab)s%(property)s:%(ws)s%(style)s;%(nl)s"
        fills.update({
            'property': self.property,
            'style': ''.join([p.format(fills) 
                              if hasattr(p, 'format') 
                              else str(p)
                              for p in self.parsed]),
        })
        return f % fills
