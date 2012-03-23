"""
"""
from .node import Node
class Variable(Node):
    def parse(self, scope):
        """
        """
        self.name = self.tokens.pop(0)
        self.value = self.tokens[1]
        if type(self.name) is tuple:
            if len(self.name) > 1:
                self.name, pad = self.name
                self.value.append(pad)
            else:
                self.name = self.name[0]
        return self
        
