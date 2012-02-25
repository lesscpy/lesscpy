"""
"""
from .node import Node
from lesscpy.lessc import utility

class Expression(Node):
    def parse(self, scope):
        """ Parse Node
            @param list: current scope
        """
        assert(len(self.tokens) == 3)
        expr = [t.parse(scope) if hasattr(t, 'parse') 
                else t
                for t in self.tokens]
        expr = [self.neg(t, scope) for t in expr]
        A, O, B = [e[0] 
                   if type(e) is tuple 
                   else e 
                   for e in expr]
        a, ua = utility.analyze_number(A, 'Illegal element in expression')
        b, ub = utility.analyze_number(B, 'Illegal element in expression')
        if(a is False or b is False):
            return ''.join([A, O, B])
        if ua == 'color' or ub == 'color':
            return color.LessColor().process(expression)
        out = self.operate(a, b, O)
        if type(a) is int and type(b) is int:
            out = int(out)
        return self.with_units(out, ua, ub)
    
    def neg(self, t, scope):
        """
        """
        if t and type(t) is list and t[0] == '-':
            v = t[1]
            if len(t) > 1 and hasattr(t[1], 'parse'):
                v = t[1].parse(scope)
            if type(v) is str:
                return '-' + v
            return -v
        return t
    
    def with_units(self, v, ua, ub):
        """
        """
        if v == 0: return v;
        if ua and ub:
            if ua == ub:
                return str(v) + ua
            else:
                raise SyntaxError("Error in expression %s != %s" % (ua, ub))
        elif ua:
            return str(v) + ua
        elif ub:
            return str(v) + ub
        return v
    
    def operate(self, a, b, o):
        """
        """
        operation = {
            '+': '__add__',
            '-': '__sub__',
            '*': '__mul__',
            '/': '__truediv__'
        }.get(o[0])
        v = getattr(a, operation)(b)
        if v is NotImplemented:
            v = getattr(b, operation)(a)
        return v
