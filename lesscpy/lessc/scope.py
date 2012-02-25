"""
"""
class Scope(list):
    def __init__(self, init=False):
        super().__init__()
        self._mixins = {}
        if init: self.push()
        
    def push(self):
        """
        """
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
        
    def add_variable(self, variable):
        """
        """
        self[-1]['__variables__'][variable.name] = variable
        
    def variables(self, name):
        """
        """
        i = len(self)
        while i >= 0:
            i -= 1
            if name in self[i]['__variables__']:
                return self[i]['__variables__'][name]
        return False
    
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
        self._mixins.update(scope._mixins)
        self[0]['__variables__'].update(scope[0]['__variables__'])
        self[0]['__blocks__'].extend([b for b in scope[0]['__blocks__']])
        