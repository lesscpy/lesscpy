"""
"""
import re
from .node import Node
from lesscpy.lessc import utility

class String(Node):
    def parse(self, scope):
        """
        """
        self.scope = scope
        return re.sub(r'@\{([^\}]+)\}', lambda m: self.swap(m.group(1)), self.tokens)
    
    def swap(self, var):
        """ Replace variable
            @param string: var
            @return: string
        """
        var = '@' + var
        var = ''.join(utility.flatten(self.scope.swap(var)))
        return var.strip("\"'")