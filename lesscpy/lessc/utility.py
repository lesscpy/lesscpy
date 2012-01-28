"""
    Utility functions
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import collections

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
        @return: tuple (number, unit)
    """
    u = None
    if type(var) is not str:
        return (var, u)
    if is_color(var):
        return (var, 'color')
    var = var.strip()
    n = var
    if not '.' in var:
        try:
            n = int(var)
            return (n, u)
        except (ValueError, TypeError):
            pass
    try:
        n = float(var)
    except (ValueError, TypeError):
        try:
            n = ''.join([c for c in var if c in '0123456789.-'])
            n = float(n) if '.' in n else int(n)
            u = ''.join([c for c in var if c not in '0123456789.-'])
        except ValueError:
            raise SyntaxError('%s ´%s´' % (err, var))
    return (n, u)

def with_unit(n, u):
    """ Return number with unit
        @param int/float: value
        @param str: unit
        @return: mixed
    """
    if n == 0: return 0
    if u:
        return "%s%s" % (str(n), u)
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
            
def print_recursive(ll, lvl=0):
    """ Scopemap printer
        @param list: parser result
        @param int: depth
    """
    if not ll: return
    pad = ''.join(['. '] * lvl)
    if type(ll) is list:
        ll = flatten(ll)
        for l in ll:
            t = type(l)
            if t == str:
                print(pad + l)
            else:
                print_recursive(l, lvl+1)
    elif hasattr(ll, '_p'):
        print(pad + str(type(ll)))
        print_recursive(ll._p, lvl+1)
    else:
        print(pad + ll)
        
            