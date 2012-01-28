"""
    LESSCSS Parser.

    http://www.dabeaz.com/ply/ply.html
    http://www.w3.org/TR/CSS21/grammar.html#scanner
    http://lesscss.org/#docs
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import os
import ply.yacc
from . import lexer
from . import utility
from .color import LessColor
from lesscpy.plib import *
    
class LessParser(object):
    precedence = (
       ('left', '+', '-'),
       ('left', '*', '/'),
    )
    def __init__(self, 
            lex_optimize=True,
            yacc_optimize=True,
            yacctab='yacctab',
            yacc_debug=False,
            scope=None,
            outputdir='/tmp',
            importlvl=0):
        """ Parser object
            @param bool: Optimized lexer
            @param bool: Optimized parser
            @param string: Yacc tables file
            @param bool: Debug mode
            @param dict: Included scope
        """
        self.importlvl = importlvl
        self.lex = lexer.LessLexer()
        if not yacctab:
            yacctab = 'yacctab'
            
        self.ignored = ('t_ws', 'css_comment', 'less_comment',
                        'css_vendor_hack', 'css_keyframes')
        
        self.tokens = [t for t in self.lex.tokens 
                       if t not in self.ignored]
        self.parser = ply.yacc.yacc(
            module=self, 
            start='unit',
            debug=yacc_debug,
            optimize=yacc_optimize,
            tabmodule=yacctab,
            outputdir=outputdir
        )
        self.scope = scope if scope else []
        self.stash = {}
        self.result = None
        self.target = None
        
    def parse(self, filename='', debuglevel=0):
        """ Parse file.
            @param string: Filename
            @param int: Debuglevel
        """
        self._create_scope()
        self.target = filename
        self.result = self.parser.parse(filename, lexer=self.lex, debug=debuglevel)
            
    def scopemap(self):
        """ Output scopemap.
        """
        if self.result:
            utility.print_recursive(self.result)
            
    def p_unit(self, p):
        """ unit                 : statement_list
        """
        p[0] = p[1]
        
    def p_statement_list_aux(self, p):
        """ statement_list       : statement_list statement
        """
        p[1].extend([p[2]])
        p[0] = p[1]
        
    def p_statement_list(self, p):
        """ statement_list       : statement
        """
        p[0] = [p[1]]
        
    def p_statement(self, p):
        """ statement            : block_decl
                                 | variable_decl
                                 | mixin_decl
        """
        p[0] = p[1]
        
    def p_statement_aux(self, p):
        """ statement            : css_charset css_string ';'
                                 | css_namespace css_string ';'
        """
        p[0] = Statement(p)
        p[0].parse(None)
        
    def p_statement_namespace(self, p):
        """ statement            : css_namespace css_ident css_string ';'
        """
        p[0] = Statement(p)
        p[0].parse(None)
        
    def p_statement_import(self, p):
        """ statement            : css_import css_string ';'
        """
        if self.importlvl > 8:
            raise ImportError('Recrusive import level too deep > 8 (circular import ?)')
        ipath = utility.destring(p[2])
        fn, fe = os.path.splitext(ipath)
        if not fe or fe.lower() == '.less':
            try:
                cpath = os.path.dirname(os.path.abspath(self.target))
                if not fe: ipath += '.less'
                filename = "%s%s%s" % (cpath, os.sep, ipath)
                if os.path.exists(filename):
                    recurse = LessParser(importlvl=self.importlvl+1)
                    recurse.parse(filename=filename, debuglevel=0)
                    self.update_scope(recurse.scope)
                else:
                    err = "Cannot import '%s', file not found" % filename
                    self.handle_error(err, p, 'W')
                p[0] = None
            except ImportError as e:
                self.handle_error(e, p)
        else:
            p[0] = Statement(p)
            p[0].parse(None)
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#              
    def p_mixin_decl(self, p):
        """ mixin_decl        : block_open_mixin declaration_list brace_close
        """
        try:
            mixin = Mixin(p)
            mixin.parse(self.scope, self.stash)
            self.scope[-1]['__mixins__'][mixin.name.strip()] = mixin
        except SyntaxError as e:
            self.handle_error(e, p)
        p[0] = None   

    def p_block_decl(self, p):
        """ block_decl         : block_open declaration_list brace_close
        """
        try:
            block = Block(p)
            block.parse(self.scope)
            self.scope[-1]['__blocks__'].append(block)
            p[0] = block
        except SyntaxError as e:
            self.handle_error(e, p)
            p[0] = None
            
    def p_block_empty(self, p):
        """ block_decl        : block_open brace_close
        """
        p[0] = None
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
        
    def p_block_open_mixin(self, p):
        """ block_open_mixin        : css_class t_popen block_mixin_args t_pclose brace_open
        """
        self.scope[-1]['current'] = '__mixin__'
        p[0] = list(p)[1:5]
        
    def p_block_open_mixin_aux(self, p):
        """ block_open_mixin        : css_class t_popen less_arguments t_pclose brace_open
        """
        self.scope[-1]['current'] = '__mixin__'
        p[0] = list(p)[1:5]
        
    def p_block_open_mixin_empty(self, p):
        """ block_open_mixin        : css_class t_popen t_pclose brace_open
        """
        self.scope[-1]['current'] = '__mixin__'
        p[0] = [p[1]]
        
    def p_block_mixin_args_aux(self, p):
        """ block_mixin_args     : block_mixin_args ',' block_mixin_arg
        """
        p[1].extend([p[2], p[3]])
        p[0] = p[1]
        
    def p_block_mixin_args(self, p):
        """ block_mixin_args     : block_mixin_arg
        """
        p[0] = [p[1]]
        
    def p_block_mixin_arg_def(self, p):
        """ block_mixin_arg     : less_variable ':' block_mixin_factor
        """
        p[0] = list(p)[1:4]
        
    def p_block_mixin_arg(self, p):
        """ block_mixin_arg     : block_mixin_factor
                                | less_variable
        """
        p[0] = p[1]
        
    def p_block_mixin_factor(self, p):
        """ block_mixin_factor  : css_number
                                | css_color
                                | css_ident
                                | css_string
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_block_open(self, p):
        """ block_open        : identifier_list brace_open
        """
        name = ["%s " % t
                if t in '>+'
                else t 
                for t in utility.flatten(p[1])]
        self.scope[-1]['current'] = ''.join(name).strip()
        p[0] = p[1]
        
    def p_identifier_list_mixin(self, p):
        """ mixin                  : identifier_list ';'
        """
        p[0] = p[1]

    def p_identifier_list(self, p):
        """ identifier_list    : identifier_group
                               | identifier_page
                               | css_font_face
        """
        if type(p[1]) is list:
            p[0] = p[1]
        else:
            p[0] = [p[1]]
            
    def p_identifier_page_aux(self, p):
        """ identifier_page    : identifier_page dom_filter
        """
        p[1].extend(p[2])
        p[0] = p[1]
            
    def p_identifier_page(self, p):
        """ identifier_page    : css_page
        """
        p[0] = [p[1]]
        
    def p_identifier_group_op(self, p):
        """ identifier_group   : identifier_group ',' identifier
                               | identifier_group '+' identifier
        """
        p[1].extend([p[2], p[3]])
        p[0] = p[1]

    def p_identifier_group_aux(self, p):
        """ identifier_group    : identifier_group identifier
        """
        p[1].extend([p[2]])
        p[0] = p[1]
        
    def p_identifier_group(self, p):
        """ identifier_group    : identifier
        """
        p[0] = [p[1]]
        
    def p_identifier_group_media(self, p):
        """ identifier_group    : css_media
        """
        p[0] = [p[1]]
        
    def p_identifier(self, p):
        """ identifier    : css_dom
                          | css_id
                          | css_class
                          | dom_filter
                          | css_color
                          | less_combine
                          | '*'
                          | '>'
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
        
    def p_declaration_list_aux(self, p):
        """ declaration_list    : declaration_list declaration
        """
        p[1].extend([p[2]])
        p[0] = p[1]
        
    def p_declaration_list(self, p):
        """ declaration_list    : declaration
        """
        p[0] = [p[1]]

    def p_declaration(self, p):
        """ declaration         : property_decl
        """
        p[0] = p[1]
        
    def p_declaration_block(self, p):
        """ declaration         : block_decl
                                | variable_decl
        """
        p[0] = p[1]
        
    def p_variable_decl(self, p):
        """ variable_decl        : less_variable ':' style_list ';'
        """
        current = self.scope[-1]
        try:
            v = Variable(p)
            v.parse(self.scope)
            if 'current' in current and current['current'] == '__mixin__':
                self.stash[v.name()] = v
            else:
                current[v.name()] = v
        except SyntaxError as e:
            print(e)
        p[0] = None
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
    def p_property_mixin_call(self, p):
        """ property_decl           : identifier_list t_popen argument_list t_pclose ';'
        """
        n = p[1][0]
        if n in self.scope[0]['__mixins__']:
            if self.scope[-1]['current'] != '__mixin__':
                try:
                    p[0] = self.scope[0]['__mixins__'][n].call(p[3], self.scope)
                except SyntaxError as e:
                    self.handle_error(e, p)
                    p[0] = None
            else:
                p[0] = self.scope[0]['__mixins__'][n] 
        else:
            self.handle_error('Mixin not found in scope: ´%s´' % n, p)
            p[0] = None
                
        
    def p_property_mixin_call_empty(self, p):
        """ property_decl           : identifier_list t_popen t_pclose ';'
        """
        n = p[1][0]
        if n in self.scope[0]['__mixins__']:
            try:
                p[0] = self.scope[0]['__mixins__'][n].call(None)
            except SyntaxError as e:
                self.handle_error(e, p)
                p[0] = None
        else:
            p[0] = None

    def p_property_mixin(self, p):
        """ property_decl           : mixin
        """
        m = ''.join([u.strip() for u in p[1]])
        l = utility.block_search(m, self.scope)
        if l:
            p[0] = [b.parsed['proplist'] for b in l]
        elif m in self.scope[0]['__mixins__']:
            try:
                p[0] = self.scope[0]['__mixins__'][m].call(None)
            except SyntaxError as e:
                self.handle_error(e, p)
                p[0] = None
        else:
            p[0] = []
            
        
    def p_property_decl(self, p):
        """ property_decl           : property ':' style_list ';'
                                    | property ':' style_list
        """
        p[0] = Property(p)
        if self.scope[-1]['current'] != '__mixin__':
            try:
                p[0].parse(self.scope)
            except SyntaxError as e:
                self.handle_error(e, p)
                p[0] = None
        
    def p_prop_decl_bad(self, p):
        """ property_decl           : property ':' ';'
        """
        p[0] = None
        
    def p_property(self, p):
        """ property    : css_property
                        | css_vendor_property
                        | css_ident
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
    def p_style_list(self, p):
        """ style_list        : style_group
        """
        p[0] = p[1]
        
    def p_less_style_list(self, p):
        """ style_list        : less_arguments
        """
        p[0] = p[1]
        
    def p_style_group_sep(self, p):
        """ style_group        : style_group ',' style
        """
        p[1].extend([p[2], p[3]])
        p[0] = p[1]
        
    def p_style_group_aux(self, p):
        """ style_group        : style_group style
        """
        p[1].extend([p[2]])
        p[0] = p[1]
        
    def p_style_group(self, p):
        """ style_group        : style
        """
        p[0] = [p[1]]
        
    def p_style(self, p):
        """ style       : expression
                        | css_important
                        | css_string
                        | istring
                        | css_vendor_property
                        | css_property
                        | css_ident
        """
        p[0] = p[1]
        
    def p_style_escape(self, p):
        """ style       : '~' istring
                        | '~' css_string
        """
        try:
            p[0] = Call(p)#.parse(self.scope)
        except SyntaxError as e:
            self.handle_error(e, p)
            p[0] = None
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_dom_filter(self, p):
        """ dom_filter    : css_dom filter_group
                          | css_id filter_group
                          | css_class filter_group
                          | less_combine filter_group
        """
        p[0] = [p[1], p[2]]
        
    def p_filter_group_aux(self, p):
        """ filter_group  : filter filter
        """
        p[1].extend([p[2]])
        p[0] = p[1]
        
    def p_filter_group(self, p):
        """ filter_group  : filter
        """
        p[0] = [p[1]]
        
    def p_filter(self, p):
        """ filter    : css_filter
                      | ':' css_ident
                      | ':' css_filter
                      | ':' ':' css_ident
        """
        p[0] = list(p)[1:]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
    def p_expression_aux(self, p):
        '''expression     : expression '+' expression
                          | expression '-' expression
                          | expression '*' expression
                          | expression '/' expression
        '''
        try:
            p[0] = Expression(p)
        except SyntaxError as e:
            print(e)
            p[0] = None
        
    def p_expression_p_neg(self, p):
        """ expression    : '-' t_popen expression t_pclose
        """
        p[0] = [p[1], p[3]]
        
    def p_expression_p(self, p):
        """ expression    : t_popen expression t_pclose
        """
        p[0] = p[2]
        
    def p_expression(self, p):
        """ expression       : factor
        """
        p[0] = p[1]
        
    def p_factor(self, p):     
        """factor           : color
                            | number
                            | variable
                            | css_dom
                            | fcall
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
        
    def p_fcall(self, p):
        """ fcall           : css_ident t_popen argument_list t_pclose
                            | css_property t_popen argument_list t_pclose
                            | css_vendor_property t_popen argument_list t_pclose
        """
        p[0] = Call(p)
        if self.scope[-1]['current'] != '__mixin__':
            try:
                p[0] = p[0].parse(self.scope)
            except SyntaxError as e:
                self.handle_error(e, p)
                p[0] = None
        
    def p_fcall_format(self, p):
        """ fcall            : less_open_format argument_list t_pclose
        """
        try:
            p[0] = Call(p).parse(self.scope)
        except SyntaxError as e:
            self.handle_error(e, p)
            p[0] = None
            
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
        
    def p_argument_list_aux_1(self, p):
        """ argument_list    : argument_list ',' argument
        """
        p[1].extend([p[2], p[3]])
        p[0] = p[1]
        
    def p_argument_list_aux(self, p):
        """ argument_list    : argument_list argument
        """
        p[1].extend([p[2]])
        p[0] = p[1]
        
    def p_argument_list(self, p):
        """ argument_list    : argument
        """
        p[0] = [p[1]]
        
    def p_argument(self, p):
        """ argument        : expression
                            | css_string
                            | istring
                            | css_ident
                            | css_id
                            | css_uri
                            | '='
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
    def p_interpolated_str(self, p):
        """ istring         : less_string
        """
        try:
            p[0] = String(p)#.parse(self.scope)
        except SyntaxError as e:
            self.handle_error(e, p, 'W')
            p[0] = p[1]
        
    def p_variable_neg(self, p):
        """ variable        : '-' variable
        """
        p[0] = '-' + p[2] 
        
    def p_variable_strange(self, p):
        """ variable        : t_popen variable t_pclose
        """
        p[0] = p[2]
        
    def p_variable(self, p):
        """ variable        : less_variable
        """
        p[0] = p[1] 
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
        
    def p_color(self, p):
        """ color            : css_color
        """
        p[0] = LessColor().format(p[1]) 
            
    def p_number(self, p):
        """ number            : css_number
                              | css_number_unit
        """ 
        p[0] = p[1] 
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
        
    def p_scope_open(self, p):
        """ brace_open          : '{'
        """
        self._create_scope()
        p[0] = p[1]
        
    def p_scope_close(self, p):
        """ brace_close        : '}'
        """
        self.scope.pop()
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def _create_scope(self):
        """ Create a scope.
        """
        self.scope.append({'__blocks__': [], '__mixins__': {}})
        
    def update_scope(self, scope):
        """
        """
        blocks = [b for b in self.scope[0]['__blocks__']]
        blocks.extend([b for b in scope[0]['__blocks__']])
        self.scope[0].update(scope[0])
        self.scope[0]['__blocks__'] = blocks

    def p_error(self, t):
        """ Internal error handler
            @param Lex token: Error token 
        """
        if t: print("E: line: %d, Syntax Error, token: `%s`, `%s`" 
                    % (t.lineno, t.type, t.value))
        while True:
            t = self.lex.token()
            if not t or t.value == '}':
                if len(self.scope) > 1:
                    self.scope.pop()
                break
        self.parser.restart()
        return t
        
    def handle_error(self, e, p, t='E'):
        """ Custom error handler
            @param Exception: Exception
            @param Parser token: Parser token
            @param string: Error level 
        """
        l = [n for n in [p.lineno(i) for i in range(len(p))] if n]
        l = l[0] if l else -1
        print("%s: line: %d: " % (t, l), end='')
        print(e)
        
