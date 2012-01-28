"""
    Property Node
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import lesscpy.lessc.utility as utility
from .process import Process

class Property(Process):
    format = "%(tab)s%(property)s:%(ws)s%(style)s;%(nl)s"
    
    def parse(self, scope):
        """ Parse Node
            @param list: current scope
        """
        self.scope = scope
        self.parsed = {}
        tokens = list(utility.flatten([self._p[1], self._p[3]]))
        self.parsed['property'] = tokens[0]
        style = self.preprocess(tokens[1:])
        style = self.process_tokens(style)
        style = ' '.join([str(t).strip() for t in style 
                          if t is not None]).replace(' , ', ', ')
        self.parsed['style'] = style
        return self
        
    def preprocess(self, style):
        """ Preprocess for annoying shorthand CSS declarations
            @param list: style
            @return: list
        """
        if self.parsed['property'] == 'font':
            style = [''.join(u.expression()) 
                     if hasattr(u, 'expression')
                     else u
                     for u in style]
        return style
        
