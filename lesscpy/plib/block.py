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
            name, inner = self.tokens
            self.name = name.parse(scope)
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
    
    def format(self, fills):
        """
        """
        out = []
        if self.parsed:
            f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(eb)s"
            name = self.name.strip()
            if fills['nl']:
                if len(name) > 80 and name.count(',') > 5:
                    name = name.replace(',', ',%s' % fills['nl'])
                else:
                    name = name.replace(',', ',%s' % fills['ws'])
            else:
                name = re.sub(' ([\+\>~]) ', '\\1', name)
            fills.update({
                'identifier': name,
                'proplist': ''.join([p.format(fills) for p in self.parsed]),
            })
            out.append(f % fills)
        if self.inner:
            out.append(''.join([p.format(fills) for p in self.inner]))
        return ''.join(out)
    
    def copy(self, to):
        """
        """
        this = copy.deepcopy(self)
        out = [p for p in this.tokens[1] if p]
        utility.rename(out, self.name, to)
        return out
