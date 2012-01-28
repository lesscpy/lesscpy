"""
    Base process Node

    Copyright (c)
    See LICENSE for details.
     <jtm@robot.is>
"""
import lesscpy.lessc.utility as utility
from .node import Node

class Process(Node):
    def __init__(self, p):
        self._p = list(p)
        self.lines = [j for j in [p.lineno(i)
                      for i in range(len(self._p))]
                      if j]
        self.scope  = None
        self.parsed = {}
        
    def process_tokens(self, tokens):
        """
        """
        while True:
            done = True
            if any(t for t in tokens if hasattr(t, 'parse')):
                tokens = [t.parse(self.scope) if hasattr(t, 'parse') 
                          else t
                          for t in tokens]
                done = False
            if any(t for t in tokens if utility.is_variable(t)):
                tokens = self.replace_vars(tokens)
                done = False
            tokens = list(utility.flatten(tokens))
            if done: break
        return tokens
        
    def replace_vars(self, tokens):
        """
        Replace variables in tokenlist
        """
        return [self.swap(t) 
                if utility.is_variable(t)
                else t
                for t in tokens]
    
    def swap(self, var):
        """ 
        Swap single variable
        """
        if not self.scope:
            raise SyntaxError("Unknown variable ´%s´" % var)
        pad = ''
        pre = ''
        if var.endswith(' '):
            var = var.strip()
            pad = ' '
        if var.startswith('-'):
            var = ''.join(var[1:])
            pre = '-'
        r = var.startswith('@@')
        t = ''.join(var[1:]) if r else var
        i = len(self.scope)
        while i >=0:
            i -= 1
            if t in self.scope[i]:
                f = self.scope[i][t].value()
                if r:
                    return self.swap("%s@%s%s" % (pre, f[0].strip('"\''), pad))
                return self.ftok(f, pre, pad)
        raise SyntaxError("Unknown variable ´%s´" % var)
    
    def ftok(self, t, pre, pad):
        """
        """
        try:
            r = ''.join(t)
        except TypeError:
            r = t[0] if type(t) is list else str(t)
        if pad and type(r) is str:
            r += pad
        if pre and type(r) is str:
            r = pre + r
        return r
    
