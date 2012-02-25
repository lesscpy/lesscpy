"""
"""
from .node import Node
from lesscpy.lessc import utility
class Block(Node):
    pass

    def parse(self, scope):
        ident, inner = self.tokens
        self.name = ident.parse(scope)
        self.parsed = [p.parse(scope) 
                       for p in inner
                       if p and type(p) is not type(self)]
        self.inner = [p.parse(scope)
                      for p in inner
                      if p and type(p) is type(self)]
        return self
    
    def format(self, fills):
        """
        """
        f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(nl)s%(endblock)s"
        fills.update({
            'identifier': self.name,
            'proplist': ''.join([p.format(fills) for p in self.parsed]),
            'endblock': ''.join([p.format(fills) for p in self.inner]),
        })
        return f % fills