"""
"""
from .node import Node

class Deferred(Node):
    def __init__(self, mixin, args):
        """
        """
        self.mixin = mixin
        self.args = args
    
    def parse(self, scope):
        """
        """
        if hasattr(self.mixin, 'call'):
            return self.mixin.call(scope, self.args)
        m = scope.mixins(self.mixin.raw())
        if m: return m.call(scope, self.args)