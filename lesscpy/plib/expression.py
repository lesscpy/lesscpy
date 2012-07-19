# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.expression
    :synopsis: Expression node.
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Johann T. Mariusson <jtm@robot.is>
"""
import sys
from .node import Node
from lesscpy.lessc import utility
from lesscpy.lessc import color

class Expression(Node):
    """Expression node. Parses all expression except
    color expressions, (handled in the color class)
    """
    
    def parse(self, scope):
        """ Parse Node
        args:
            scope (Scope): Scope object
        raises:
            SyntaxError
        returns:
            str
        """
        assert(len(self.tokens) == 3)
        expr = self.process(self.tokens, scope)
        expr = [self.neg(t, scope) for t in expr]
        A, O, B = [e[0] 
                   if type(e) is tuple 
                   else e 
                   for e in expr
                   if str(e).strip()]
        try:
            a, ua = utility.analyze_number(A, 'Illegal element in expression')
            b, ub = utility.analyze_number(B, 'Illegal element in expression')
        except SyntaxError:
            return ' '.join([str(A), str(O), str(B)])
        if(a is False or b is False):
            return ' '.join([str(A), str(O), str(B)])
        if ua == 'color' or ub == 'color':
            return color.Color().process((A, O, B))
        out = self.operate(a, b, O)
        if type(out) is bool:
            return out
        return self.with_units(out, ua, ub)
    
    def neg(self, value, scope):
        """Apply negativity.
        args:
            value (mixed): test value
            scope (Scope): Current scope
        raises:
            SyntaxError
        returns:
            str
        """
        if value and type(value) is list and value[0] == '-':
            val = value[1]
            if len(value) > 1 and hasattr(value[1], 'parse'):
                val = value[1].parse(scope)
            if type(val) is str:
                return '-' + val
            return -val
        return value
    
    def with_units(self, val, ua, ub):
        """Return value with unit. 
        args:
            val (mixed): result
            ua (str): 1st unit
            ub (str): 2nd unit
        raises:
            SyntaxError
        returns:
            str
        """
        if not val: return str(val)
        if ua or ub:
            if ua and ub:
                if ua == ub:
                    return str(val) + ua
                else:
                    # Nodejs version does not seem to mind mismatched 
                    # units within expressions. So we choose the first
                    # as they do
                    # raise SyntaxError("Error in expression %s != %s" % (ua, ub))
                    return str(val) + ua
            elif ua:
                return str(val) + ua
            elif ub:
                return str(val) + ub
        return str(val)
    
    def operate(self, vala, valb, oper):
        """Perform operation
        args:
            vala (mixed): 1st value
            valb (mixed): 2nd value
            oper (str): operation
        returns:
            mixed
        """
        operation = {
            '+': '__add__',
            '-': '__sub__',
            '*': '__mul__',
            '/': '__truediv__',
            '=': '__eq__',
            '>': '__gt__',
            '<': '__lt__',
            '>=': '__ge__',
            '<=': '__le__',
            '!=': '__ne__',
            '<>': '__ne__',
        }.get(oper)
        if sys.version_info[0] < 3:
            ret = self.py2op(vala, operation, valb)
        else:
            ret = getattr(vala, operation)(valb)
        if ret is NotImplemented:
            ret = getattr(valb, operation)(vala)
        if oper in '+-*/':
            try:
                if int(ret) == ret:
                    return int(ret)
            except ValueError:
                pass
        return ret
    
    def py2op(self, vala, operation, valb):
        """ Python2 operators
        """
        if   operation == '__lt__':
            ret = (vala < valb)
        elif operation == '__gt__':
            ret = (vala > valb)
        elif operation == '__eq__':
            ret = (vala == valb)
        elif operation == '__ge__':
            ret = (vala >= valb)
        elif operation == '__le__':
            ret = (vala <= valb)
        elif operation == '__ne__':
            ret = (vala != valb)
        else:
            ret = getattr(vala, operation)(valb)
        return ret
    
    def expression(self):
        """Return str representation of expression
        returns:
            str
        """
        return utility.flatten(self.tokens)
