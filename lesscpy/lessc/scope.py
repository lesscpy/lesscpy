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
        
    def current(self):
        return self[-1]['__current__']
    
    def mixin(self, mixin):
        """
        """
        return self[0]['__mixins__'][mixin] if mixin in self[0]['__mixins__'] else False