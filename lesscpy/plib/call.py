"""
"""
import re
from urllib.parse import quote as urlquote
from .node import Node
import lesscpy.lessc.utility as utility
import lesscpy.lessc.color as Color

class Call(Node):
    def parse(self, scope):
        name = ''.join(self.tokens.pop(0))
        parsed = self.process(self.tokens, scope)
        if name == '%(':
            name = 'sformat'
        elif name == '~':
            name = 'e'
        color = Color.LessColor()
        args = [t for t in parsed 
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
        return name + ''.join([p for p in parsed])
    
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
