"""
"""
from lesscpy.lessc import utility
class Node(object):
    def __init__(self, p, ln=0):
        self.tokens = p
        self.lineno = ln
        self.parsed = False
    
    def parse(self, scope):
        return self
    
    def process(self, tokens, scope):
        """
        """
        while True:
            tokens = list(utility.flatten(tokens))
            done = True
            if any(t for t in tokens if hasattr(t, 'parse')):
                tokens = [t.parse(scope) 
                          if hasattr(t, 'parse') 
                          else t
                          for t in tokens]
                done = False
            if any(t for t in tokens if utility.is_variable(t)):
                tokens = self.replace_variables(tokens, scope)
                done = False
            if done: break
        return tokens
    
    def replace_variables(self, tokens, scope):
        """
        """
        return [scope.swap(t)
                if utility.is_variable(t)
                else t 
                for t in tokens]

    def fmt(self, fills):
        raise ValueError('No defined format')
