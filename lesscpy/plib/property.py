"""
"""
from .node import Node
from lesscpy.lessc import utility

class Property(Node):
    def parse(self, scope):
        """
        """
        if not self.parsed:
            if len(self.tokens) > 2:
                property, style, _ = self.tokens
                self.important = True
            else:
                property, style = self.tokens
                self.important = False
            self.property = ''.join(property)
            self.parsed = []
            if style:
                style = self.preprocess(style)
                self.parsed = self.process(style, scope)
        return self
    
    def preprocess(self, style):
        """
        Hackish preprocessing from font shorthand tags.
        """
        if self.property == 'font':
            style = [''.join(u.expression()) 
                     if hasattr(u, 'expression')
                     else u
                     for u in style]
        else:
            style = [(u, ' ')
                     if hasattr(u, 'expression')
                     else u
                     for u in style]
        return style
        
    def format(self, fills):
        """
        """
        f = "%(tab)s%(property)s:%(ws)s%(style)s%(important)s;%(nl)s"
        imp = ' !important' if self.important else ''
        if fills['nl']:
            self.parsed = [',%s' % fills['ws']
                           if p == ','
                           else p 
                           for p in self.parsed]
        style = ''.join([p.format(fills) 
                         if hasattr(p, 'format') 
                         else str(p)
                         for p in self.parsed])
        fills.update({
            'property': self.property,
            'style': style.strip(),
            'important': imp
        })
        return f % fills
