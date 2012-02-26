"""
"""
from .node import Node
from lesscpy.lessc import utility
class Identifier(Node):
    def parse(self, scope):
        """
        """
        scopename = scope.scopename if scope else []
        name = ''.join([t + ' '
                        if t in '*>~+'
                        else t 
                        for t in utility.flatten(self.tokens)])
        self.real = name
        scopename.append(name)
        return ''.join(scopename).replace(' &', '')
