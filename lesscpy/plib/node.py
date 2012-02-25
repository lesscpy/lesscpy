"""
"""
class Node(object):
    def __init__(self, p):
        self.tokens = p
    
    def parse(self, scope):
        return self

    def format(self, fills):
        return str(type(self))
