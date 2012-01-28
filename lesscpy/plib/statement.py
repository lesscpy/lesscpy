"""
    Statement Node
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
from .process import Process

class Statement(Process):
    format = "%(identifier)s%(ws)s%(value)s;%(nl)s"
    
    def parse(self, scope):
        """ Parse Node
            @param list: current scope
        """
        self._ident = self._p[1].strip()
        self.parsed['identifier'] = self._ident
        self.parsed['value'] = self._p[2]
    
