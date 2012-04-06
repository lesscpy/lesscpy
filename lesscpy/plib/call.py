# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.call
    :synopsis: Call parse node
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Jóhann T. Maríusson <jtm@robot.is>
"""
import re, math
from urllib.parse import quote as urlquote, urlparse
from .node import Node
import lesscpy.lessc.utility as utility
import lesscpy.lessc.color as Color
from lesscpy.lib.colors import lessColors

class Call(Node):
    """Call node. Node represents a function call.
    All builtin none-color functions are in this node.
    This node attempts calls on built-ins and lets non-builtins
    through.
    increment(3px) --> 4px
    unknown(3px) -->  unknown(3px)
    """
    
    def parse(self, scope):
        """Parse Node within scope.
        the functions ~( and e( map to self.escape
        and %( maps to self.sformat
        args:
            scope (Scope): Current scope
        """
        if not self.parsed:
            name = ''.join(self.tokens[0])
            parsed = self.process(self.tokens[1:], scope)

            if name == '%(':
                name = 'sformat'
            elif name in ('~', 'e'):
                name = 'escape'
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
    
    def escape(self, string, *args):
        """Less Escape.
        args:
            string (str): string to escape
        returns:
            str
        """
        return utility.destring(string.strip('~'))
    
    def sformat(self, string, *args):
        """ String format.
        args:
            string (str): string to format
            args (list): format options
        returns:
            str
        """
        if not args:
            raise SyntaxError('Not enough arguments...')
        format = string
        items = []
        m = re.findall('(%[asdA])', format)
        i = 0
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
    
    def isnumber(self, string, *args):
        """Is number
        args:
            string (str): match
        returns:
            bool
        """
        try:
            n, u = utility.analyze_number(string)
        except SyntaxError as e:
            return False
        return True
    
    def iscolor(self, string, *args):
        """Is color
        args:
            string (str): match
        returns:
            bool
        """
        return (string in lessColors)
    
    def isurl(self, string, *args):
        """Is url
        args:
            string (str): match
        returns:
            bool
        """
        arg = utility.destring(string)
        regex = re.compile(r'^(?:http|ftp)s?://' # http:// or https://
                           r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                           r'localhost|' #localhost...
                           r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                           r'(?::\d+)?' # optional port
                           r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return regex.match(arg)
    
    def isstring(self, string, *args):
        """Is string
        args:
            string (str): match
        returns:
            bool
        """
        regex = re.compile(r'\'[^\']*\'|"[^"]*"')
        return regex.match(string)
    
    def iskeyword(self, string, *args):
        """Is less keyword
        args:
            string (str): match
        returns:
            bool
        """
        return (string in ('when', 'and', 'not'))
    
    def increment(self, value, *args):
        """ Increment function
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(n+1, u)
    
    def decrement(self, value, *args):
        """ Decrement function
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(n-1, u)
    
    def add(self, *args):
        """ Add integers
        args:
            args (list): target
        returns:
            str
        """
        if(len(args) <= 1): return 0
        return sum([int(v) for v in args])
    
    def round(self, value, *args):
        """ Round number
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(round(float(n)), u)
    
    def ceil(self, value, *args):
        """ Ceil number
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(math.ceil(n), u)
    
    def floor(self, value, *args):
        """ Floor number
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        return utility.with_unit(math.floor(n), u)
    
    def percentage(self, value, *args):
        """ Return percentage value
        args:
            value (str): target
        returns:
            str
        """
        n, u = utility.analyze_number(value)
        n = int(n * 100.0)
        u = '%'
        return utility.with_unit(n, u)
