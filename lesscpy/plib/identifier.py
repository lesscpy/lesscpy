"""
"""
from .node import Node
from lesscpy.lessc import utility
class Identifier(Node):
    def parse(self, scope):
        """
        """
        name = ''.join([t + ' '
                        if t in '*>~+'
                        else t 
                        for t in utility.flatten(self.tokens)])
        names = self.root(scope, name) if scope else [name]
        self.real = name
        return ','.join(names)
    
    def root(self, scope, name):
        """
        """
        names = [p.strip()
                 for p in name.split(',')]
        parent = scope.scopename
        if parent: 
            parent.reverse()
            for p in parent:
                parts = p.split(',')
                names = [n.replace('&', p.strip())
                         if '&' in n
                         else
                         "%s %s" % (p.strip(), n)
                         for n in names 
                         for p in parts]
        return names
        
