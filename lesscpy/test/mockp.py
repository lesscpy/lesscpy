
class Mockp(object):
    def __init__(self, l):
        self.l = [None]
        self.l.extend(l)
        
    def __iter__(self):
        return self.l.__iter__()
    
    def next(self):
        return self.l.next()
    
    def lineno(self, n):
        return 1