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
        mixins = scope.mixins(self.mixin.raw())
        if not mixins: return mixins
        for m in mixins:
            res = m.call(scope, self.args)
            if res: return res
