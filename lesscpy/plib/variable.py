"""
    Variable Node

    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
from .process import Process

class Variable(Process):
    def name(self):
        return self._p[1]
        
    def value(self):
        return self._p[3]
        
    def parse(self, scope):
        return ''