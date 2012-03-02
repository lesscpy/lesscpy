"""
"""
import re, copy
from .node import Node
from lesscpy.lessc import utility
class Block(Node):
    pass

    def parse(self, scope):
        """
        """
        print('parse block')
        if not self.parsed:
            self.name, inner = self.tokens
            if not inner: inner = []
            self.parsed = [p.parse(scope) 
                           for p in inner
                           if p and type(p) is not type(self)]
            if not inner: 
                self.inner = []
            else:
               self. inner = [p for p in inner 
                         if p and type(p) is type(self)]
            if self.inner:
                self.inner = [p.parse(scope) for p in self.inner]
        return self
    
    def raw(self):
        return self.name.raw()
    
    def format(self, fills):
        """
        """
        out = []
        if self.parsed:
            f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(eb)s"
            name = self.name.format(fills)
            fills.update({
                'identifier': name,
                'proplist': ''.join([p.format(fills) for p in self.parsed]),
            })
            out.append(f % fills)
        if self.inner:
            out.append(''.join([p.format(fills) for p in self.inner]))
        return ''.join(out)
    
    def copy(self, scope):
        """
        """
        this = copy.deepcopy(self)
        scope = copy.deepcopy(scope)
        out = [p for p in this.tokens[1] if p]
        utility.rename(out, self.name, scope)
        return out
