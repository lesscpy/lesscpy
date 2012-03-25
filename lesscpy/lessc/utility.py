"""
    Utility functions
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import collections
import re

def flatten(ll):
    """
    Flatten list.
    @param ll: list
    @return: generator
    """
    for el in ll:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            for sub in flatten(el):
                yield sub
        else:
            yield el
            
def pairwise(lst):
    """ yield item i and item i+1 in lst. e.g.
        (lst[0], lst[1]), (lst[1], lst[2]), ..., (lst[-1], None)
    """
    if not lst: return
    l = len(lst)
    for i in range(l-1):
        yield lst[i], lst[i+1]
    yield lst[-1], None
    
def rename(ll, scope):
    """ Rename all sub-blocks moved under another 
        block. (mixins)
    """
    for p in ll:
        if hasattr(p, 'inner'):
            p.name.parse(scope)
            if p.inner: 
                scope.push()
                scope.current = p.name
                rename(p.inner, scope)
                scope.pop()
            
def blocksearch(block, name):
    """ Recursive search for name in block
    """
    for b in block.inner:
        b = (b if b.raw() == name 
             else blocksearch(b, name))
        if b: return b
    return False

def reverse_guard(ll):
    """
    """
    rev = {
        '<': '>',
        '>': '<',
        '=': '!=',
        '!=': '=',
        '>=': '<=',
        '<=': '>='
    }
    return [rev[l] if l in rev else l for l in ll]

def debug_print(ll, lvl=0):
    """
    """
    pad = ''.join(['\t.'] * lvl)
    t = type(ll)
    if t is list:
        for p in ll:
            debug_print(p, lvl)
    elif hasattr(ll, 'tokens'):
        print(pad, t) 
        debug_print(list(flatten(ll.tokens)), lvl+1)

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
    if len(v) in [4, 5, 7, 9]:
        try:
            int(v[1:], 16)
            return True
        except Exception:
            pass
    return False
            
def is_variable(v):
    """ Check if string is LESS variable
        @param string: check
        @return: bool
    """
    if type(v) is str:
        return (v.startswith('@') or v.startswith('-@'))
    elif type(v) is tuple:
        v = ''.join(v)
        return (v.startswith('@') or v.startswith('-@'))
    return False

def is_int(v):
    """ Is value integer
    """
    try:
        int(str(v))
        return True
    except (ValueError, TypeError):
        pass
    return False

def is_float(v):
    """ Is value float
    """
    if not is_int(v):
        try:
            float(str(v))
            return True
        except (ValueError, TypeError):
            pass
    return False

def split_unit(v):
    """ Split a number from its unit
    """
    r = re.search('^(\-?[\d\.]+)(.*)$', str(v))
    return r.groups() if r else ('','')
    
    
            