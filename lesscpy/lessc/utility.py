"""
    Utility functions
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import collections
import re

def flatten(l):
    """
    Flatten list.
    @param l: list
    @return: generator
    """
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            for sub in flatten(el):
                yield sub
        else:
            yield el
            
def block_search(name, scope):
    """ Search scope blocks for name
        @param str: name
        @param list: scope
        @return: list
    """
    def search(m, l):
        """
        """
        prop = []
        for b in l:
            n = b._cident
            if m == n:
                prop.append(b)
            elif m in b._parts:
                prop.append(b)
            elif m.startswith(n):
                r = search(m, b.parsed['inner'])
                if r: prop.extend(r)
        return prop
    l = len(scope)
    i = 1
    prop = []
    while (l-i) >= 0:
        if scope[-i]['__blocks__']:
            b = search(name, scope[-i]['__blocks__'])
            if b: prop.extend(b)
        i += 1 
    # HACK
    if '>' in name:
        name = ''.join([c for c in name if c != '>'])
        i = 0
        while (l-i) >= 0:
            if scope[-i]['__blocks__']:
                b = search(name, scope[-i]['__blocks__'])
                if b: prop.extend(b)
            i += 1 
    return prop

def destring(v):
    """ Strip quotes
        @param string: value
        @return: string
    """
    return v.strip('"\'')

def analyze_number(var, err=''):
    """ Analyse number for type and split from unit
        @param str: value
        @raises: SyntaxError
        @return: tuple (number, unit)
    """
    n, u = split_unit(var)
    if type(var) is not str:
        return (var, u)
    if is_color(var):
        return (var, 'color')
    if is_int(n):
        n = int(n)
    elif is_float(n):
        n = float(n)
    else:
        raise SyntaxError('%s ´%s´' % (err, var))
    return (n, u)

def with_unit(n, u=None):
    """ Return number with unit
        @param int/float: value
        @param str: unit
        @return: mixed
    """
    if type(n) is tuple:
        n, u = n
    if n == 0: return 0
    if u:
        n = str(n)
        if n.startswith('.'):
            n = '0' + n 
        return "%s%s" % (n, u)
    return n
            
def is_color(v):
    """ Is CSS color
        @param mixed: value
        @return: bool
    """
    if not v or type(v) is not str: 
        return False
    l = len(v)
    if l == 4 or l == 7:
        try:
            int(v[1:], 16)
            return True
        except Exception:
            return False
            
def is_variable(v):
    """ Check if string is LESS variable
        @param string: check
        @return: bool
    """
    if type(v) is str:
        return (v.startswith('@') or v.startswith('-@'))
    return False

def is_int(v):
    """
    """
    try:
        int(str(v))
        return True
    except (ValueError, TypeError):
        pass
    return False

def is_float(v):
    """
    """
    if not is_int(v):
        try:
            float(str(v))
            return True
        except (ValueError, TypeError):
            pass
    return False

def split_unit(v):
    """
    """
    r = re.search('^(\-?[\d\.]+)(.*)$', str(v))
    return r.groups() if r else ('','')
    
    
            