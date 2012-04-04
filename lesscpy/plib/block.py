# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.block
    :synopsis: Block parse node.
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Jóhann T. Maríusson <jtm@robot.is>
"""
import re, copy
from .node import Node
from lesscpy.lessc import utility

class Block(Node):
    """ Block node. Represents one parse-block.
    Can contain property nodes or other block nodes.
    identifier {
        propertys
        inner blocks
    }
    """
    def parse(self, scope):
        """Parse block node.
        args:
            scope (Scope): Current scope
        raises:
            SyntaxError
        returns:
            self
        """
        if not self.parsed:
            self.name, inner = self.tokens
            if not inner: inner = []
            self.parsed = [p.parse(scope) 
                           for p in inner
                           if p and type(p) is not type(self)]
            self.parsed = list(utility.flatten(self.parsed))
            if not inner: 
                self.inner = []
            else:
               self. inner = [p for p in inner 
                              if p and type(p) is type(self)]
            if self.inner:
                self.inner = [p.parse(scope) for p in self.inner]
        return self
    
    def raw(self, clean=False):
        """Raw block name
        args:
            clean (bool): clean name
        returns:
            str
        """
        try:
            return self.name.raw(clean)
        except AttributeError:
            pass
    
    def fmt(self, fills):
        """Format block (CSS)
        args:
            fills (dict): Fill elements
        returns:
            str (CSS)
        """
        f = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(eb)s"
        out = []
        name = self.name.fmt(fills)
        if self.parsed:
            fills.update({
                'identifier': name,
                'proplist': ''.join([p.fmt(fills) for p in self.parsed]),
            })
            out.append(f % fills)
        if self.inner:
            if self.name.subparse: # @media
                inner = ''.join([p.fmt(fills) for p in self.inner])
                inner = inner.replace(fills['nl'], 
                                      fills['nl'] + fills['tab']).rstrip(fills['tab'])
                fills.update({
                    'identifier': name,
                    'proplist': fills['tab'] + inner,
                })
                out.append(f % fills)
            else:
                out.append(''.join([p.fmt(fills) for p in self.inner]))
        return ''.join(out)
    
    def copy(self, scope):
        """Copy block contents (properties, inner blocks). 
        Renames inner block from current scope.
        Used for mixins.
        args: 
            scope (Scope): Current scope
        returns:
            list (block contents)
        """
        if self.tokens[1]:
            tokens = copy.deepcopy(self.tokens[1])
            out = [p for p in tokens if p]
            utility.rename(out, scope)
            return out
        return None
