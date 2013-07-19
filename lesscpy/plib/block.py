# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.block
    :synopsis: Block parse node.

    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Johann T. Mariusson <jtm@robot.is>
"""
import re
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
            scope.push()
            self.name, inner = self.tokens
            scope.current = self.name
            scope.real.append(self.name)
            if not self.name.parsed:
                self.name.parse(scope)
            if not inner:
                inner = []
            inner = list(utility.flatten([p.parse(scope) for p in inner if p]))
            self.parsed = [p for p in inner if p and not isinstance(p, Block)]
            self.inner = [p for p in inner if p and isinstance(p, Block)]
            scope.real.pop()
            scope.pop()
        return self

    def raw(self, clean=False):
        """Raw block name
        args:
            clean (bool): clean name
        returns:
            str
        """
        try:
            return self.tokens[0].raw(clean)
        except (AttributeError, TypeError):
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
                'proplist': ''.join([p.fmt(fills) for p in self.parsed if p]),
            })
            out.append(f % fills)
        if hasattr(self, 'inner'):
            if self.name.subparse:  # @media
                inner = ''.join([p.fmt(fills) for p in self.inner])
                inner = inner.replace(fills['nl'],
                                      fills['nl'] + fills['tab']).rstrip(fills['tab'])
                if not fills['nl']:
                    inner = inner.strip()
                fills.update({
                    'identifier': name,
                    'proplist': fills['tab'] + inner
                })
                out.append(f % fills)
            else:
                out.append(''.join([p.fmt(fills) for p in self.inner]))
        return ''.join(out)

    def copy(self):
        """ Return a full copy of self
        returns: Block object
        """
        name, inner = self.tokens
        if inner:
            inner = [u.copy() if u else u
                     for u in inner]
        if name:
            name = name.copy()
        return Block([name, inner], 0)

    def copy_inner(self, scope):
        """Copy block contents (properties, inner blocks).
        Renames inner block from current scope.
        Used for mixins.
        args:
            scope (Scope): Current scope
        returns:
            list (block contents)
        """
        if self.tokens[1]:
            tokens = [u.copy() if u else u
                      for u in self.tokens[1]]
            out = [p for p in tokens if p]
            utility.rename(out, scope, Block)
            return out
        return None
