"""
"""
import copy
from .node import Node
from lesscpy.lessc import utility
class Block(Node):
    pass

    def parse(self, scope):
        """
        """
        scope = copy.deepcopy(scope)
        ident, inner = self.tokens
        self.name = ident.parse(scope)
        if not inner: inner = []
        self.parsed = [p.parse(scope) 
                       for p in inner
                       if p and type(p) is not type(self)]
        scope.current = self.name
        self.inner = [p.parse(scope)
                      for p in inner
                      if p and type(p) is type(self)]
        return self
    
    def format(self, fills):
        """
        """
        out = []
        if self.parsed:
            f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(nl)s"
            fills.update({
                'identifier': self.name.strip(),
                'proplist': ''.join([p.format(fills) for p in self.parsed]),
            })
            out.append(f % fills)
        if self.inner:
            out.append(''.join([p.format(fills) for p in self.inner]))
        return ''.join(out)
