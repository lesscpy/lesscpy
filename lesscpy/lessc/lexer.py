"""
    Lexer for LESSCSS.
    
    http://www.dabeaz.com/ply/ply.html
    http://www.w3.org/TR/CSS21/grammar.html#scanner
    http://lesscss.org/#docs
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import re
import ply.lex as lex

from lesscpy.lib import dom
from lesscpy.lib import css

class LessLexer:
    states = (
      ('parn', 'inclusive'),
    )
    literals = ',<>{}=%!/*-+:;~&';
    tokens = [
        'css_ident',
        'css_dom',
        'css_class',
        'css_id',
        'css_property',
        'css_vendor_property',
        'css_comment',
        'css_string',
        'css_color',
        'css_filter',
        'css_number',
        'css_important',
        'css_vendor_hack',
        'css_uri',
        'css_ms_filter',
        
        'less_variable',
        'less_comment',
        'less_string',
        'less_open_format',
        'less_when',
        'less_and',
        'less_not',
        
        't_ws',
        't_popen',
        't_pclose',
    ]
    reserved = {
        '@media' : 'css_media',
        '@page': 'css_page',
        '@import' : 'css_import',
        '@charset' : 'css_charset',
        '@font-face' : 'css_font_face',
        '@namespace' : 'css_namespace',
        '@keyframes' : 'css_keyframes',
        '@-moz-keyframes' : 'css_keyframes',
        '@-webkit-keyframes' : 'css_keyframes',
        '@-ms-keyframes' : 'css_keyframes',
        
        '@arguments': 'less_arguments',
    }
    tokens += list(set(reserved.values()))
    # Tokens with significant following whitespace
    significant_ws = [
        'css_class', 
        'css_id', 
        'css_dom',
        'css_property',
        'css_vendor_property',
        'css_ident',
        'css_number',
        'css_color',
        'less_variable',
        '&',
    ]
    significant_ws += list(set(reserved.values()))
    
    def __init__(self):
        self.build(reflags=re.UNICODE|re.IGNORECASE)
        self.last = None
        self.next = None
        self.pretok = True
        
    def t_css_filter(self, t):
        (r'\[[^\]]*\]'
        '|(not|lang|nth-[a-z\-]+)\(.+\)'
        '|and[ \t]\([^><]+\)')
        return t
    
    def t_css_ms_filter(self, t):
        r'progid:[^;]*'
        return t
        
    def t_css_ident(self, t):
        (r'([\-\.\#]?'
         '|@[@\-]?)'
         '([_a-z]'
         '|[\200-\377]'
         '|\\\[0-9a-f]{1,6}'
         '|\\\[^\s\r\n0-9a-f])'
         '([_a-z0-9\-]'
         '|[\200-\377]'
         '|\\\[0-9a-f]{1,6}'
         '|\\\[^\s\r\n0-9a-f])*')
        v = t.value.strip()
        c = v[0]
        if c == '.':
            t.type = 'css_class'
        elif c == '#':
            t.type = 'css_id'
            if len(v) in [4, 7]:
                try:
                    int(v[1:], 16)
                    t.type = 'css_color'
                except ValueError:
                    pass
        elif v == 'when':
            t.type = 'less_when'
        elif v == 'and':
            t.type = 'less_and'
        elif v == 'not':
            t.type = 'less_not'
        elif v in css.propertys:
            t.type = 'css_property'
            t.value = t.value.strip()
        elif v.lower() in dom.html:
            t.type = 'css_dom'
        elif c == '@':
            v = v.lower()
            if v in LessLexer.reserved:
                t.type = LessLexer.reserved[v]
            else:
                t.type = 'less_variable'
        elif c == '-':
            t.type = 'css_vendor_property'
        t.value = t.value.strip()
        return t
    
    def t_less_variable(self, t):
        r'@\w+'
        return t
    
    def t_css_color(self, t):
        r'\#[0-9]([0-9a-f]{5}|[0-9a-f]{2})'
        return t
    
    def t_css_number(self, t):
        r'-?(\d*\.\d+|\d+)(s|%|in|ex|[ecm]m|p[txc]|deg|g?rad|ms?|k?hz)?'
        return t
    
    def t_parn_css_uri(self, t):
        (r'data:[^\)]+'
         '|(([a-z]+://)?'
         '('
         '([\.a-z:]+[\w\.:]*[\\/][\\/]?)+'
         '|([a-z][\w\.\-]+(\.[a-z0-9]+))'
         '(\#[a-z]+)?)'
         ')+')
        return t
    
    def t_parn_css_ident(self, t):
        (r'(([_a-z]'
         '|[\200-\377]'
         '|\\\[0-9a-f]{1,6}'
         '|\\\[^\r\n\s0-9a-f])'
         '([_a-z0-9\-]|[\200-\377]'
         '|\\\[0-9a-f]{1,6}'
         '|\\\[^\r\n\s0-9a-f])*)')
        return t
    
    def t_newline(self, t):
        r'[\n\r]+'
        t.lexer.lineno += t.value.count('\n')
        
    def t_css_comment(self, t):
        r'(/\*(.|\n|\r)*?\*/)'
        t.lexer.lineno += t.value.count('\n')
        pass

    def t_less_comment(self, t):
        r'//.*'
        pass
    
    def t_css_important(self, t):
        r'!\s*important'
        t.value = '!important'
        return t
    
    def t_t_ws(self, t):
        r'[ \t\f\v]+'
        t.value = ' '
        return t

    def t_t_popen(self, t):
        r'\('
        t.lexer.push_state('parn')
        return t
    
    def t_less_open_format(self, t):
        r'%\('
        t.lexer.push_state('parn')
        return t
    
    def t_t_pclose(self, t):
        r'\)'
        t.lexer.pop_state()
        return t
    
    def t_less_string(self, t):
        (r'"([^"@]*@\{[^"\}]+\}[^"]*)+"'
        '|\'([^\'@]*@\{[^\'\}]+\}[^\']*)+\'')
        t.lexer.lineno += t.value.count('\n')
        return t
    
    def t_css_string(self, t):
        r'"[^"]*"|\'[^\']*\''
        t.lexer.lineno += t.value.count('\n')
        return t
    
    # Error handling rule
    def t_error(self, t):
        raise SyntaxError("Illegal character '%s' line %d" % (t.value[0], t.lexer.lineno))
        t.lexer.skip(1)
        
    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)    
            
    def file(self, filename):
        """
        Lex file.
        """
        with open(filename) as f:
            self.lexer.input(f.read())
        return self
    
    def input(self, filename):
        """
        Wrapper for file
        """
        with open(filename) as f:
            self.lexer.input(f.read())
            
    def token(self):
        """
        Token function. Contains 2 hacks:
            1.  Injects ';' into blocks where the last property
                leaves out the ;
            2.  Strips out whitespace from nonsignificant locations
                to ease parsing.
        """
        if self.next:
            t = self.next
            self.next = None
            return t
        while True:
            t = self.lexer.token()
            if not t: return t
            if t.type == 't_ws' and (
                self.pretok or (self.last 
                and self.last.type not in self.significant_ws)):
                continue
            self.pretok = False
            if t.type == '}' and self.last and self.last.type not in '{;}':
                self.next = t
                tok = lex.LexToken()
                tok.type = ';'
                tok.value = ';'
                tok.lineno = t.lineno
                tok.lexpos = t.lexpos
                self.last = tok
                return tok
            self.last = t
            break
        return t
