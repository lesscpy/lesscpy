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
            
def rename(ll, fr, scope):
    """ Rename all sub-blocks moved under another 
        block. (mixins)
    """
    for p in ll:
        if hasattr(p, 'inner'):
            p.name.parse(scope)
            scope.push()
            scope.current = p.name
            if p.inner: rename(p.inner, fr, scope)
            
def blocksearch(block, name):
    """
    """
    print('blocksearch', name)
    for b in block.inner:
        print('cmp', b.raw(), name)
        if b.raw() == name:
            return b
        else:#if name.startswith(b.name):
            return blocksearch(b, name)
    return False

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
    
    
            