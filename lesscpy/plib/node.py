"""
    Parser node base class.
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
class Node(object):
    def name(self):
        """ @return: node name"""
        return self._name
        
    def value(self):
        """ @return: node value"""
        return self._value
        
    def parse(self, scope):
        raise NotImplementedError()