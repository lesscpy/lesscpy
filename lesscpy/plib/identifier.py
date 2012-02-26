"""
"""
from .node import Node
from lesscpy.lessc import utility
class Identifier(Node):
    def parse(self, scope):
        """
        """
        scopename = []
        if scope:
            scopename.extend(scope.scopename)
        scopename = ''.join(scopename)
        name = ''.join([t + ' '
                        if t in '*>~+'
                        else t 
                        for t in utility.flatten(self.tokens)])
        if name.startswith('&'):
            scopename = scopename.strip()
            name = name[1:]
        return scopename + name
