"""
    Call Node.
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import re
from urllib.parse import quote as urlquote
from .process import Process
from lesscpy.lessc.color import LessColor
from .expression import Expression
import lesscpy.lessc.utility as utility

class Call(Process):
    def parse(self, scope):
        """ Parse Node
            @param list: current scope
        """
        self.scope = scope
        call = list(utility.flatten(self._p[1:]))
        name = call[0]
        if name == '%(':
            name = 'sformat'
        elif name == '~':
            name = 'e'
        color = LessColor()
        call = self.process_tokens(call[1:])
        args = [t for t in call 
                if type(t) is not str or t not in '(),']
        if hasattr(self, name):
            try:
                return getattr(self, name)(*args)
            except ValueError:
                pass
        if hasattr(color, name):
            try:
                return getattr(color, name)(*args)
            except ValueError:
                pass
        call = ' '.join([str(t) for t in call[1:-1]]).replace(' = ', '=')
        return ["%s(%s)" % (name, call)]
    
    def e(self, string):
        """ Less Escape.
            @param string: value
            @return string
        """
        return utility.destring(string.strip('~'))
    
    def sformat(self, *args):
        """ String format
            @param list: values
            @return string
        """
        format = args[0]
        items = []
        m = re.findall('(%[asdA])', format)
        i = 1
        for n in m:
            v = {
              '%d' : int,
              '%A' : urlquote,
              '%s' : utility.destring,
            }.get(n, str)(args[i])
            items.append(v)
            i += 1
        format = format.replace('%A', '%s')
        return format % tuple(items)
    
    def increment(self, v):
        """ Increment function
            @param Mixed: value
            @return: incremented value
        """
        n, u = utility.analyze_number(v)
        return utility.with_unit(n+1, u)
    
    def decrement(self, v):
        """ Decrement function
            @param Mixed: value
            @return: incremented value
        """
        n, u = utility.analyze_number(v)
        return utility.with_unit(n-1, u)
    
    def add(self, *args):
        """ Add integers
            @param list: values
            @return: int
        """
        return sum([int(v) for v in args])
    
    def round(self, v):
        """ Round number
            @param Mixed: value
            @return: rounded value
        """
        n, u = utility.analyze_number(v)
        return utility.with_unit(round(float(n)), u)
    