"""
    Block node.
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
from collections import OrderedDict

import lesscpy.lessc.utility as utility
from .process import Process

class Block(Process):
    format = "%(identifier)s%(ws)s{%(nl)s%(proplist)s}%(endblock)s"
    
    def parse(self, scope):
        """ Parse Node
            @param list: current scope
        """
        self._blocktype = None
        self.scope = scope
        self._proplist()
        self.parsed['inner'] = [p for p in self._p[2] 
                                if type(p) is type(self)]
        self._pname()
        if self._name.startswith('@media'):
            self._blocktype = 'inner'
        self.parsed['identifier'] = self._ident.strip()
        return self
    
    def merge(self, block):
        """
        """
        assert(type(block) is Block)
        self.parsed['proplist'].extend(block.parsed['proplist'])
    
    def _pname(self):
        """ Parse block name and identifier
        """
        name = ["%s " % t
                if t in '>+'
                else t 
                for t in utility.flatten(self._p[1])]
        self._name = ''.join(name)
        self._ident = self._fullname(name)
        self._cident = self._ident.replace(' ', '')
        
    def _fullname(self, name):
        """
        """
        parent = list(utility.flatten([s['current'] 
                                       for s in self.scope 
                                       if 'current' in s]))
        if parent: 
            parent.reverse()
            if parent[-1].startswith('@media'):
                parent.pop()
        names = [p.strip()
                 for p in self._name.split(',')]
        self._parts = names
        for p in parent:
            parts = p.split(',')
            names = [n.replace('&', p)
                     if '&' in n
                     else
                     "%s %s" % (p.strip(), n)
                     for n in names 
                     for p in parts]
        return ', '.join(names) if len(names) < 6 else ',\n'.join(names)
    
    def _proplist(self):
        """ Reduce property list to remove redundant styles.
            Multiple porperties of the same type overwrite, 
            so we can safely take only the last.
        """
        proplist = [p for p in utility.flatten(self._p[2]) 
                    if p and type(p) != type(self)]
        store = OrderedDict()
        for p in proplist:
            store[p.parsed['property']] = p
        self.parsed['proplist'] = store.values()
