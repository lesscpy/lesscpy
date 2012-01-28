"""
    Expression Node.
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import lesscpy.lessc.utility as utility
from .process import Process
from lesscpy.lessc import color

class Expression(Process):
    def parse(self, scope):
        """ Parse Node
            @param list: current scope
        """
        self.scope = scope
        expr = [self._p[1], self._p[2], self._p[3]]
        while True:
            done = True
            expr = [self.neg(t) for t in expr]
            if any(t for t in expr if hasattr(t, 'parse')):
                expr = [t.parse(scope) if hasattr(t, 'parse') 
                         else t
                         for t in expr]
                done = False
            if any(t for t in expr if utility.is_variable(t)):
                expr = self.replace_vars(expr)
                done = False
            expr = list(utility.flatten(expr))
            if done: break
        p = self.process(expr)
        return p
    
    def neg(self, t):
        """
        """
        if t and type(t) is list and t[0] == '-':
            v = t[1]
            if len(t) > 1 and hasattr(t[1], 'parse'):
                v = t[1].parse(self.scope)
            if type(v) is str:
                return '-' + v
            return -v
        return t
    
    def process(self, expression):
        """
        """
        assert(len(expression) == 3)
        A, O, B = expression
        a, ua = utility.analyze_number(A, 'Illegal element in expression')
        b, ub = utility.analyze_number(B, 'Illegal element in expression')
        if(a is False or b is False):
            return self.expression()
        if ua == 'color' or ub == 'color':
            return color.LessColor().process(expression)
        out = self.operate(a, b, O)
        if type(a) is int and type(b) is int:
            out = int(out)
        return self.units(out, ua, ub)
    
    def units(self, v, ua, ub):
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
#        print("´%s´ ´%s´ ´%s´" % (a, b, o))
        operation = {
            '+': '__add__',
            '-': '__sub__',
            '*': '__mul__',
            '/': '__truediv__'
        }.get(o)
        v = getattr(a, operation)(b)
        if v is NotImplemented:
            v = getattr(b, operation)(a)
        return v
    
    def expression(self):
        """
        """
        return [self._p[1], self._p[2], self._p[3]]
    
            
            
            