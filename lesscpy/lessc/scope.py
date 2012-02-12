"""
"""
class Scope(list):
    def __init__(self):
        super().__init__()
        
    def push(self):
        self.append({
            '__variables__' : {},
            '__blocks__': [], 
            '__mixins__': {}, 
            '__current__': None
        })
        
    @property
    def current(self):
        return self[-1]['__current__']
    
    @current.setter
    def current(self, value):
        self[-1]['__current__'] = value
    
    def mixin(self, mixin):
        """
        """
        return self[0]['__mixins__'][mixin] if mixin in self[0]['__mixins__'] else False
    
    def in_mixin(self):
        """
        """
        return any([s for s in self 
                    if s['__current__'] == '__mixin__'])