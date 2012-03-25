"""
    Calls to builtin functions.
"""
import re, math
from urllib.parse import quote as urlquote, urlparse
from .node import Node
import lesscpy.lessc.utility as utility
import lesscpy.lessc.color as Color
from lesscpy.lib.colors import lessColors

class Call(Node):
    def parse(self, scope):
        """
        Parse Node within scope
        """
        if not self.parsed:
            name = ''.join(self.tokens[0])
            parsed = self.process(self.tokens[1:], scope)
            if name == '%(':
                name = 'sformat'
            elif name == '~':
                name = 'e'
            color = Color.Color()
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
            self.parsed = name + ''.join([p for p in parsed])
        return self.parsed
    
    def e(self, *args):
        """ Less Escape.
            @param string: value
            @return string
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        return utility.destring(args[0].strip('~'))
    
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
    
    def isnumber(self, *args):
        """
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        try:
            n, u = utility.analyze_number(args[0])
        except SyntaxError as e:
            return False
        return True
    
    def iscolor(self, *args):
        """
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        return (args[0] in lessColors)
    
    def isurl(self, *args):
        """
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        arg = utility.destring(args[0])
        regex = re.compile(r'^(?:http|ftp)s?://' # http:// or https://
                           r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                           r'localhost|' #localhost...
                           r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                           r'(?::\d+)?' # optional port
                           r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return regex.match(arg)
    
    def isstring(self, *args):
        """
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        regex = re.compile(r'\'[^\']*\'|"[^"]*"')
        return regex.match(args[0])
    
    def iskeyword(self, *args):
        """
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        return (args[0] in ('when', 'and', 'not'))
    
    def increment(self, *args):
        """ Increment function
            @param Mixed: value
            @return: incremented value
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        n, u = utility.analyze_number(args[0])
        return utility.with_unit(n+1, u)
    
    def decrement(self, *args):
        """ Decrement function
            @param Mixed: value
            @return: incremented value
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        n, u = utility.analyze_number(args[0])
        return utility.with_unit(n-1, u)
    
    def add(self, *args):
        """ Add integers
            @param list: values
            @return: int
        """
        if(len(args) <= 1):
            raise SyntaxError('Wrong number of arguments')
        return sum([int(v) for v in args])
    
    def round(self, *args):
        """ Round number
            @param Mixed: value
            @return: rounded value
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        n, u = utility.analyze_number(args[0])
        return utility.with_unit(round(float(n)), u)
    
    def ceil(self, *args):
        """ Ceil number
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        n, u = utility.analyze_number(args[0])
        return utility.with_unit(math.ceil(n), u)
    
    def floor(self, *args):
        """ Floor number
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        n, u = utility.analyze_number(args[0])
        return utility.with_unit(math.floor(n), u)
    
    def percentage(self, *args):
        """ Return percentage value
        """
        if(len(args) > 1):
            raise SyntaxError('Wrong number of arguments')
        n, u = utility.analyze_number(args[0])
        n = int(n * 100.0)
        u = '%'
        return utility.with_unit(n, u)
