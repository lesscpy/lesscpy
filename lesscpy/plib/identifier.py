"""
"""
import re
from .node import Node
from lesscpy.lessc import utility
class Identifier(Node):
    def parse(self, scope):
        """
        """
        names       = []
        name        = []
        if self.tokens and self.tokens[0] == '@media':
            name = list(utility.flatten(self.tokens))
        else:
            for n in utility.flatten(self.tokens):
                if n == '*':
                    name.append('* ')
                elif n in '>+~':
                    if name and name[-1] == ' ':
                        name.pop()
                    name.append('?%s?' % n)
                elif n == ',':
                    names.append(name)
                    name = []
                else:
                    name.append(n)
        names.append(name)
        parsed = self.root(scope, names) if scope else names
        self.parsed = [[i for i, j in utility.pairwise(part) 
                        if i != ' ' or (j and '?' not in j)] 
                       for part in parsed]
        return self
    
    def root(self, scope, names):
        """
        """
        parent = scope.scopename
        if parent: 
            parent = parent[-1]
            return [self._pscn(part, n) 
                    if part[0] != '@media'
                    else n
                    for part in parent.parsed
                    for n in names]
        return names
    
    def _pscn(self, parent, name):
        """
        """
        parsed = []
        if any((n for n in name if n == '&')):
            for n in name:
                if n == '&':
                    if parent[-1] == ' ':
                        parent.pop()
                    parsed.extend(parent)
                else:
                    parsed.append(n)
        else:
            parsed.extend(parent)
            if parent[-1] != ' ':
                parsed.append(' ')
            parsed.extend(name)
        return parsed
    
    def raw(self, clean=False):
        """
        """
        if clean: return ''.join(''.join(p) for p in self.parsed).replace('?', ' ')
        return '%'.join('%'.join(p) for p in self.parsed).strip().strip('%')
        
    
    def fmt(self, fills):
        """
        """
        name = ',$$'.join(''.join(p).strip() 
                          for p in self.parsed)
        name = re.sub('\?(.)\?', '%(ws)s\\1%(ws)s', name) % fills
        return (name.replace('$$', fills['nl']) 
                if len(name) > 85 
                else name.replace('$$', fills['ws'])).replace('  ', ' ')
    
        
