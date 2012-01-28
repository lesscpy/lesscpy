"""
    String Node
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import re
from .process import Process

class String(Process):
    def parse(self, scope):
        """ Parse Node
            @param list: current scope
            @return: string
        """
        self.scope = scope
        return re.sub(r'@\{([^\}]+)\}', lambda m: self.format(m.group(1)), self._p[1])
    
    def format(self, var):
        """ Format variable for replacement
            @param string: var
            @return: string
        """
        var = '@' + var
        var = self.swap(var)
        return var.strip("\"'")
