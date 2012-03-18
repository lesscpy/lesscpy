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
    
    def raw(self, clean=False):
        """
        """
        try:
            return self.name.raw(clean)
        except AttributeError:
            pass
    
    def fmt(self, fills):
        """
        """
        f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(eb)s"
        out = []
        name = self.name.fmt(fills)
        if self.parsed:
            fills.update({
                'identifier': name,
                'proplist': ''.join([p.fmt(fills) for p in self.parsed]),
            })
            out.append(f % fills)
        if self.inner:
            if name.startswith('@media'):
                inner = ''.join([p.fmt(fills) for p in self.inner])
                inner = inner.replace(fills['nl'], 
                                      fills['nl'] + fills['tab']).rstrip(fills['tab'])
                fills.update({
                    'identifier': name,
                    'proplist': fills['tab'] + inner,
                })
                out.append(f % fills)
            else:
                out.append(''.join([p.fmt(fills) for p in self.inner]))
                
        return ''.join(out)
    
    def copy(self, scope):
        """
        """
        if self.tokens[1]:
            tokens = copy.deepcopy(self.tokens[1])
            scope = copy.deepcopy(scope)
            out = [p for p in tokens if p]
            utility.rename(out, scope)
            return out
        return None
