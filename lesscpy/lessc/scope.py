"""
"""
class Scope(list):
    def __init__(self):
        super().__init__()
        self._mixins = {}
        
    def push(self):
        self.append({
            '__variables__' : {},
            '__blocks__': [], 
            '__current__': None
        })
        
    @property
    def current(self):
        return self[-1]['__current__']
    
    @current.setter
    def current(self, value):
        self[-1]['__current__'] = value
        
    def add_block(self, block):
        """
        """
        self[-1]['__blocks__'].append(block)
        
    def add_mixin(self, mixin):
        """
        """
        self._mixins[mixin.name()] = mixin
    
    def mixins(self, name):
        """
        """
        return (self._mixins[name] 
                if name in self._mixins
                else False)
    
    def in_mixin(self):
        """
        """
        return any([s for s in self 
                    if s['__current__'] == '__mixin__'])
        
    def update(self, scope):
        """
        """
        blocks = [b for b in self[0]['__blocks__']]
        blocks.extend([b for b in scope[0]['__blocks__']])
        self._mixins.update(scope._mixins)
        self[0].update(scope[0])
        self[0]['__blocks__'] = blocks
        