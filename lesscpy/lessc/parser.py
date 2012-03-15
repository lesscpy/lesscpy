"""
.. module:: parser
    :synopsis: Lesscss parser.

    http://www.dabeaz.com/ply/ply.html
    http://www.w3.org/TR/CSS21/grammar.html#scanner
    http://lesscss.org/#docs
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Jóhann T. Maríusson <jtm@robot.is>
"""
import os
import copy
import ply.yacc
from . import lexer
from . import utility
from .scope import Scope
from .color import Color
from lesscpy.plib import *
    
class LessParser(object):
    precedence = (
       ('left', '+', '-'),
       ('left', '*', '/'),
    )
    def __init__(self, 
            lex_optimize=True,
            yacc_optimize=True,
            tabfile='yacctab',
            yacc_debug=False,
            scope=None,
            outputdir='/tmp',
            importlvl=0,
            verbose=False):
        """ Parser object
            
            Kwargs:
                lex_optimize (bool): Optimize lexer
                yacc_optimize (bool): Optimize parser
                tabfile (str): Yacc tab filename
                yacc_debug (bool): yacc debug mode
                scope (Scope): Inherited scope
                outputdir (str): Output (debugging)
                importlvl (int): Import depth
                verbose (bool): Verbose mode
        """
        self.verbose = verbose
        self.importlvl = importlvl
        self.lex = lexer.LessLexer()
        if not tabfile:
            tabfile = 'yacctab'
            
        self.ignored = ('css_comment', 'less_comment',
                        'css_vendor_hack', 'css_keyframes',
                        'css_page')
        
        self.tokens = [t for t in self.lex.tokens 
                       if t not in self.ignored]
        self.parser = ply.yacc.yacc(
            module=self, 
            start='tunit',
            debug=yacc_debug,
            optimize=yacc_optimize,
            tabmodule=tabfile,
            outputdir=outputdir
        )
        self.scope = scope if scope else Scope()
        self.stash = {}
        self.result = None
        self.target = None
        
    def parse(self, filename='', debuglevel=0):
        """ Parse file.
            @param string: Filename
            @param int: Debuglevel
        """
        if self.verbose: print('Compiling target: %s' % filename)
        self.scope.push()
        self.target = filename
        self.result = self.parser.parse(filename, lexer=self.lex, debug=debuglevel)
            
    def scopemap(self):
        """ Output scopemap.
        """
        if self.result:
            self._scopemap_aux(self.result)
            
    def _scopemap_aux(self, ll, lvl=0):
        pad = ''.join(['\t.'] * lvl)
        t = type(ll)
        if t is list:
            for p in ll:
                self._scopemap_aux(p, lvl)
        elif hasattr(ll, 'tokens'):
            if t is Block:
                print(pad, ll.name) 
            else:
                print(pad, t) 
            self._scopemap_aux(list(utility.flatten(ll.tokens)), lvl+1)
    
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#            

    def p_tunit(self, p):
        """ tunit                    : unit_list
        """
        p[0] = p[1]
        
    def p_unit_list(self, p):
        """ unit_list                : unit_list unit
                                     | unit
        """
        if len(p) == 3:
            p[1].append(p[2])
        else:
            p[1] = [p[1]] 
        p[0] = p[1]
        
    def p_unit(self, p):
        """ unit                     : statement
                                     | variable_decl
                                     | block_decl
                                     | mixin_decl
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    
        
    def p_statement_aux(self, p):
        """ statement            : css_charset t_ws css_string ';'
                                 | css_namespace t_ws css_string ';'
        """
        p[0] = Statement(list(p)[1:], p.lineno(1))
        p[0].parse(None)
        
    def p_statement_namespace(self, p):
        """ statement            : css_namespace t_ws word css_string ';'
        """
        p[0] = Statement(list(p)[1:], p.lineno(1))
        p[0].parse(None)
        
    def p_statement_import(self, p):
        """ statement            : css_import t_ws css_string ';'
                                 | css_import t_ws css_string dom ';'
        """
        if self.importlvl > 8:
            raise ImportError('Recrusive import level too deep > 8 (circular import ?)')
        ipath = utility.destring(p[3])
        fn, fe = os.path.splitext(ipath)
        if not fe or fe.lower() == '.less':
            try:
                cpath = os.path.dirname(os.path.abspath(self.target))
                if not fe: ipath += '.less'
                filename = "%s%s%s" % (cpath, os.sep, ipath)
                if os.path.exists(filename):
                    recurse = LessParser(importlvl=self.importlvl+1, verbose=self.verbose)
                    recurse.parse(filename=filename, debuglevel=0)
                    self.scope.update(recurse.scope)
                else:
                    err = "Cannot import '%s', file not found" % filename
                    self.handle_error(err, p.lineno(1), 'W')
                p[0] = None
            except ImportError as e:
                self.handle_error(e, p)
        else:
            p[0] = Statement(list(p)[1:], p.lineno(1))
            p[0].parse(None)
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

    def p_block(self, p):
        """ block_decl               : block_open declaration_list brace_close
        """
        try:
            block = Block(list(p)[1:-1], p.lineno(3))
            block.parse(self.scope)
            p[0] = block
        except SyntaxError as e:
            self.handle_error(e, p.lineno(3))
            p[0] = None
        self.scope.pop()
        self.scope.add_block(block)
            
    def p_block_replace(self, p):
        """ block_decl               : identifier ';'
        """
        m = p[1].parse(None)
        block = self.scope.blocks(m.raw())
        if block:
            p[0] = block.copy(self.scope)
        else:
            mixin = self.scope.mixins(m.raw())
            if mixin:
                try:
                    p[0] = mixin.call(self.scope)
                except SyntaxError as e:
                    self.handle_error(e, p.lineno(2))
            else:
                self.handle_error('Call unknown mixin `%s`' % p[1], p.lineno(2))
        
    def p_block_open(self, p):
        """ block_open                : identifier brace_open
        """
        p[1].parse(self.scope)
        p[0] = p[1]
        self.scope.current = p[1]
        
    def p_font_face_open(self, p):
        """ block_open                : css_font_face t_ws brace_open
        """
        p[0] = Identifier([p[1], p[2]])
        

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
    def p_mixin(self, p):
        """ mixin_decl                : open_mixin declaration_list brace_close
        """
        self.scope.add_mixin(Mixin(list(p)[1:], p.lineno(3)).parse(self.scope))
        self.scope.pop()
        p[0] = None

    def p_open_mixin(self, p):
        """ open_mixin                : class t_popen mixin_args t_pclose brace_open
                                      | id t_popen mixin_args t_pclose brace_open
        """
        p[0] = [p[1][0], p[3]]
        
    def p_call_mixin(self, p):
        """ call_mixin                : class t_popen mixin_args t_pclose ';'
                                      | id t_popen mixin_args t_pclose ';'
        """
        mixin = self.scope.mixins(p[1][0])
        if mixin:
            try:
                p[0] = mixin.call(self.scope, p[3])
            except SyntaxError as e:
                self.handle_error(e, p.lineno(2))
        else:
            self.handle_error('Call unknown mixin `%s`' % p[1], p.lineno(2))
            
    def p_mixin_args_arguments(self, p):
        """ mixin_args                : less_arguments
        """
        p[0] = [p[1]]

    def p_mixin_args_aux(self, p):
        """ mixin_args                : mixin_args ',' argument
                                      | mixin_args ',' mixin_kwarg
                                      | mixin_args argument
                                      | mixin_args mixin_kwarg
        """
        p[1].extend(list(p)[2:])
        p[0] = p[1]

    def p_mixin_args(self, p):
        """ mixin_args                : argument
                                      | mixin_kwarg
        """
        p[0] = [p[1]]
        
    def p_mixin_args_empty(self, p):
        """ mixin_args                : empty
        """
        p[0] = None
        
    def p_mixin_kwarg(self, p):
        """ mixin_kwarg                : variable ':' argument
        """
        p[0] = Variable(list(p)[1:], p.lineno(2))
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

    def p_declaration_list(self, p):
        """ declaration_list           : declaration_list declaration
                                       | declaration
                                       | empty
        """
        if len(p) > 2:
            p[1].extend(p[2])
        p[0] = p[1]
        
    def p_declaration(self, p):
        """ declaration                : variable_decl
                                       | property_decl
                                       | block_decl
                                       | mixin_decl
                                       | call_mixin
        """
        p[0] = p[1] if type(p[1]) is list else [p[1]]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

    def p_variable_decl(self, p):
        """ variable_decl            : variable ':' style_list ';'
        """
        try:
            v = Variable(list(p)[1:], p.lineno(4))
            v.parse(self.scope)
            if self.scope.in_mixin():
                self.stash[v.name] = v
            else:
                self.scope.add_variable(v)
        except SyntaxError as e:
            self.handle_error(e, p)
        p[0] = None
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_property_decl(self, p):
        """ property_decl           : prop_open style_list ';'
                                    | prop_open style_list css_important ';'
                                    | prop_open empty ';'
        """
        l = len(p)
        p[0] = Property(list(p)[1:-1], p.lineno(l-1))
        
    def p_property_decl_arguments(self, p):
        """ property_decl           : prop_open less_arguments ';'
        """
        p[0] = Property([p[1], [p[2]]], p.lineno(3))
        
    def p_prop_open_ie_hack(self, p):
        """ prop_open               : '*' prop_open
        """
        p[0] = (p[1][0], p[2][0])
        
    def p_prop_open(self, p):
        """ prop_open               : property ':'
                                    | vendor_property ':'
                                    | word ':'
        """
        p[0] = (p[1][0], '')
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
    
    def p_style_list_aux(self, p):
        """ style_list              : style_list style
                                    | style_list ',' style
                                    | style_list t_ws style
        """
        p[1].extend(list(p)[2:])
        p[0] = p[1]
        
    def p_style_list(self, p):
        """ style_list              : style
        """
        p[0] = [p[1]]
        
    def p_style(self, p):
        """ style                   : expression
                                    | css_string
                                    | word
                                    | property
                                    | vendor_property
                                    | istring
                                    | fcall
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_identifier(self, p):
        """ identifier                : identifier_list
        """
        p[0] = Identifier(p[1], 0)

    def p_identifier_list_aux(self, p):
        """ identifier_list           : identifier_list ',' identifier_group
        """
        p[1].extend([p[2]])
        p[1].extend(p[3])
        p[0] = p[1]
        
    def p_identifier_list(self, p):
        """ identifier_list           : identifier_group
        """
        p[0] = p[1]
        
    def p_identifier_group_op(self, p):
        """ identifier_group          : identifier_group child_selector ident_parts
                                      | identifier_group '+' ident_parts
                                      | identifier_group general_sibling_selector ident_parts
                                      | identifier_group '*'
        """
        p[1].extend([p[2]])
        if len(p) > 3: p[1].extend(p[3])
        p[0] = p[1]
        
    def p_identifier_group(self, p):
        """ identifier_group          : ident_parts
        """
        p[0] = p[1]
        
    def p_ident_parts_aux(self, p):
        """ ident_parts               : ident_parts ident_part
                                      | ident_parts filter_group
        """
        if type(p[2]) is list:
            p[1].extend(p[2])
        else: p[1].append(p[2])
        p[0] = p[1]
        
    def p_ident_parts(self, p):
        """ ident_parts               : ident_part
                                      | selector
                                      | filter_group
        """
        if type(p[1]) is not list:
            p[1] = [p[1]]
        p[0] = p[1]
        
    def p_ident_media(self, p):
        """ ident_parts               : css_media t_ws
        """
        p[0] = list(p)[1:]
        
    def p_selector(self, p):
        """ selector                  : '*'
                                      | '+'
                                      | child_selector
                                      | general_sibling_selector
        """
        p[0] = p[1]
        
    def p_ident_part(self, p):
        """ ident_part                : class
                                      | id
                                      | dom
                                      | combinator
                                      | color
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_filter_group_aux(self, p):
        """ filter_group              : filter_group filter
        """
        p[1].extend(p[2])
        p[0] = p[1]
        
    def p_filter_group(self, p):
        """ filter_group              : filter
        """
        p[0] = p[1]

    def p_filter(self, p):
        """ filter                    : css_filter
                                      | ':' word
                                      | ':' vendor_property
                                      | ':' css_filter
                                      | ':' ':' word
                                      | ':' ':' vendor_property
        """
        p[0] = list(p)[1:]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
        
    def p_fcall(self, p):
        """ fcall           : word t_popen argument_list t_pclose
                            | property t_popen argument_list t_pclose
                            | vendor_property t_popen argument_list t_pclose
                            | less_open_format argument_list t_pclose
                            | '~' istring
                            | '~' css_string
        """
        p[0] = Call(list(p)[1:], 0)
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_argument_list_empty(self, p):
        """ argument_list       : empty
        """
        p[0] = ''
        
    def p_argument_list_aux(self, p):
        """ argument_list       : argument_list argument
                                | argument_list ',' argument
        """
        p[1].extend(list(p)[2:])
        p[0] = p[1]
        
    def p_argument_list(self, p):
        """ argument_list       : argument
        """
        p[0] = [p[1]]
        
    def p_argument(self, p):
        """ argument        : expression
                            | css_string
                            | istring
                            | word
                            | id
                            | css_uri
                            | '='
                            | fcall
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_expression_aux(self, p):
        """ expression             : expression '+' expression
                                   | expression '-' expression
                                   | expression '/' expression
                                   | expression '*' expression
                                   | word '/' expression
        """
        p[0] = Expression(list(p)[1:], 0)
        
    def p_expression_p_neg(self, p):
        """ expression             : '-' t_popen expression t_pclose
        """
        p[0] = [p[1], p[3]]
        
    def p_expression_p(self, p):
        """ expression             : t_popen expression t_pclose
        """
        p[0] = p[2]
        
    def p_expression(self, p):
        """ expression              : factor
        """
        p[0] = p[1]
        
    def p_factor(self, p):     
        """ factor                  : color
                                    | number
                                    | variable
                                    | css_dom
        """
        p[0] = p[1]
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_interpolated_str(self, p):
        """ istring                 : less_string
        """
        p[0] = String(p[1], p.lineno(1))
        
    def p_variable_neg(self, p):
        """ variable                : '-' variable
        """
        p[0] = '-' + p[2] 
        
    def p_variable_strange(self, p):
        """ variable                : t_popen variable t_pclose
        """
        p[0] = p[2]
        
    def p_variable(self, p):
        """ variable                : less_variable
                                    | less_variable t_ws
        """
        p[0] = p[1] 

    def p_color(self, p):
        """ color                   : css_color
                                    | css_color t_ws
        """
        try:
            p[0] = Color().fmt(p[1]) 
            if len(p) > 2: p[0] = [p[0], p[2]]
        except ValueError:
            self.handle_error('Illegal color value `%s`' % p[1], p.lineno(1), 'W')
            p[0] = p[1]
        
    def p_number(self, p):
        """ number                    : css_number
                                      | css_number t_ws
        """ 
        p[0] = tuple(list(p)[1:]) 
        
    def p_dom(self, p):
        """ dom                       : css_dom
                                      | css_dom t_ws
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_word(self, p):
        """ word                      : css_ident
                                      | css_ident t_ws
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_class(self, p):
        """ class                     : css_class
                                      | css_class t_ws
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_id(self, p):
        """ id                        : css_id
                                      | css_id t_ws
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_property(self, p):
        """ property                  : css_property
                                      | css_property t_ws
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_vendor_property(self, p):
        """ vendor_property           : css_vendor_property
                                      | css_vendor_property t_ws
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_combinator(self, p):
        """ combinator                : '&' t_ws
                                      | '&'
        """
        p[0] = tuple(list(p)[1:]) 
        
        
    def p_child_selector(self, p):
        """ child_selector            : '>' t_ws
                                      | '>'
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_general_sibling_selector(self, p):
        """ general_sibling_selector  : '~' t_ws
                                      | '~'
        """
        p[0] = tuple(list(p)[1:]) 
        
    def p_scope_open(self, p):
        """ brace_open                : '{'
        """
        self.scope.push()
        p[0] = p[1]
        
    def p_scope_close(self, p):
        """ brace_close               : '}'
        """
        p[0] = p[1]
        
    def p_empty(self, p):
        'empty                        :'
        pass
        
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  

    def p_error(self, t):
        """ Internal error handler
            @param Lex token: Error token 
        """
        if t and self.verbose: 
            print("E: %s line: %d, Syntax Error, token: `%s`, `%s`" 
                  % (self.target, t.lineno, t.type, t.value))
        while True:
            t = self.lex.token()
            if not t or t.value == '}':
                if len(self.scope) > 1:
                    self.scope.pop()
                break
        self.parser.restart()
        return t
        
    def handle_error(self, e, line, t='E'):
        """ Custom error handler
            @param Exception: Exception
            @param Parser token: Parser token
            @param string: Error level 
        """
        if self.verbose:
            print("%s: line: %d: " % (t, line), end='')
            print(e)
            
