# -*- coding: utf8 -*-
"""
.. module:: lesscpy.lessc.parser
    :synopsis: Lesscss parser.

    http://www.dabeaz.com/ply/ply.html
    http://www.w3.org/TR/CSS21/grammar.html#scanner
    http://lesscss.org/#docs

    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Johann T. Mariusson <jtm@robot.is>
"""

from __future__ import print_function

import os
import sys
import ply.yacc

from . import lexer
from . import utility
from .scope import Scope
from .color import Color
from lesscpy.plib import Block, Call, Deferred, Expression, Identifier, Mixin, Property, Statement, Variable


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
                 verbose=False,
                 error_reporter=None,
                 ):
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
                        'css_vendor_hack')

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

        if error_reporter is None:
            error_reporter = _DefaultErrorReporter()
        self.error_reporter = error_reporter

    def parse(self, filename=None, file=None, debuglevel=0):
        """ Parse file.
        kwargs:
            filename (str): File to parse
            debuglevel (int): Parser debuglevel
        """
        self.scope.push()

        if not file:
            # We use a path.
            file = filename
        else:
            # We use a stream and try to extract the name from the stream.
            if hasattr(file, 'name'):
                if filename is not None:
                    raise AssertionError(
                        'names of file and filename are in conflict')
                filename = file.name()
            else:
                filename = '(stream)'

        self.target = filename
        if self.verbose:
            print('Compiling target: %s' % filename, file=sys.stderr)
        self.result = self.parser.parse(
            file, lexer=self.lex, debug=debuglevel)

        self.post_parse()

    def post_parse(self):
        """ Post parse cycle. nodejs version allows calls to mixins
        not yet defined or known to the parser. We defer all calls
        to mixins until after first cycle when all names are known.
        """
        if self.result:
            out = []
            for pu in self.result:
                try:
                    out.append(pu.parse(self.scope))
                except SyntaxError as e:
                    value = 'SyntaxError %s' % (e)
                    self.error_reporter.error(
                        filename=self.target,
                        line_no=p.lineno(1),
                        value=value,
                        )
            self.result = list(utility.flatten(out))

    def scopemap(self):
        """ Output scopemap.
        """
        utility.debug_print(self.result)

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_tunit(self, p):
        """ tunit                    : unit_list
        """
        p[0] = [u for u in p[1] if u]

    def p_unit_list(self, p):
        """ unit_list                : unit_list unit
                                     | unit
        """
        if isinstance(p[1], list):
            if len(p) >= 3:
                if isinstance(p[2], list):
                    p[1].extend(p[2])
                else:
                    p[1].append(p[2])
        else:
            p[1] = [p[1]]
        p[0] = p[1]

    def p_unit(self, p):
        """ unit                     : statement
                                     | variable_decl
                                     | block_decl
                                     | mixin_decl
                                     | call_mixin
                                     | import_statement
        """
        p[0] = p[1]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_statement_aux(self, p):
        """ statement            : css_charset t_ws css_string t_semicolon
                                 | css_namespace t_ws css_string t_semicolon
        """
        p[0] = Statement(list(p)[1:], p.lineno(1))
        p[0].parse(None)

    def p_statement_namespace(self, p):
        """ statement            : css_namespace t_ws word css_string t_semicolon
        """
        p[0] = Statement(list(p)[1:], p.lineno(1))
        p[0].parse(None)

    def p_statement_import(self, p):
        """ import_statement     : css_import t_ws string t_semicolon
                                 | css_import t_ws css_string media_query_list t_semicolon
                                 | css_import t_ws fcall t_semicolon
                                 | css_import t_ws fcall media_query_list t_semicolon

        """
        """
        @import statements may be treated differently by Less depending on
        the file extension:

        - If the file has a .css extension it will be treated as CSS and the
          @import statement left as-is (see the inline option below).
        - If it has any other extension it will be treated as Less and
          imported.
        - If it does not have an extension, .less will be appended and it
          will be included as a imported Less file.

        Reference:
        http://lesscss.org/features/#import-directives-feature-file-extensions
        """
        if self.importlvl > 8:
            raise ImportError(
                'Recrusive import level too deep > 8 (circular import ?)')

        import_path = None
        if isinstance(p[3], str):
            # css_string
            import_path = utility.destring(p[3])
        if isinstance(p[3], list):
            # string
            import_path = utility.resolve_variables(self.scope, p[3][1])
        elif isinstance(p[3], Call):
            # fcall
            # NOTE(saschpe): Always in the form of 'url("...");', so parse it
            # and retrieve the inner css_string. This whole func is messy.
            p[3] = p[3].parse(self.scope)  # Store it as string, Statement.fmt expects it.
            import_path = utility.destring(p[3][4:-1])

        name, extension = os.path.splitext(import_path)
        if extension and extension.lower() == '.css':
            p[0] =  Statement(list(p)[1:], p.lineno(1))
            p[0].parse(None)
        else:
            p[0] = self._import(import_path, line_no=p.lineno(1))

    def _import(self, import_path, line_no):
        """
        Import file at `path`.

        Returned parsed tokens or None if file could not be parsed.
        """
        name, extension = os.path.splitext(import_path)
        try:
            base_path = os.path.dirname(os.path.abspath(self.target))
            if not extension:
                import_path += '.less'
            full_path = os.path.join(base_path, import_path)
            return self._parseImport(full_path, line_no=line_no)

        except ImportError as e:
            self.error_reporter.error(
                filename=self.target,
                line_no=line_no,
                value=e,
                )
            return None

    def _parseImport(self, path, line_no):
        """
        Parse imported file at `path`.
        """
        if not os.path.exists(path):
            error = "Cannot import '%s', file not found" % path
            self.error_reporter.warning(
                filename=self.target,
                line_no=line_no,
                value=error,
                )
            return None

        recurse = LessParser(importlvl=self.importlvl + 1,
                             verbose=self.verbose, scope=self.scope)
        recurse.parse(filename=path, debuglevel=0)
        return recurse.result

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_block(self, p):
        """ block_decl               : block_open declaration_list brace_close
        """
        p[0] = Block(list(p)[1:-1], p.lineno(3))
        self.scope.pop()
        self.scope.add_block(p[0])

    def p_block_replace(self, p):
        """ block_decl               : identifier t_semicolon
        """
        m = p[1].parse(None)
        block = self.scope.blocks(m.raw())
        if block:
            p[0] = block.copy_inner(self.scope)
        else:
            # fallback to mixin. Allow calls to mixins without parens
            p[0] = Deferred(p[1], None, p.lineno(2))

    def p_block_open(self, p):
        """ block_open                : identifier brace_open
        """
        try:
            p[1].parse(self.scope)
        except SyntaxError:
            pass
        p[0] = p[1]
        self.scope.current = p[1]

    def p_block_open_media_query(self, p):
        """ block_open                : media_query_decl brace_open
        """
        p[0] = Identifier(p[1]).parse(self.scope)

    def p_font_face_open(self, p):
        """ block_open                : css_font_face t_ws brace_open
        """
        p[0] = Identifier([p[1], p[2]]).parse(self.scope)

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
        """ open_mixin                : identifier t_popen mixin_args_list t_pclose brace_open
                                      | identifier t_popen mixin_args_list t_pclose mixin_guard brace_open
        """
        p[1].parse(self.scope)
        self.scope.current = p[1]
        p[0] = [p[1], p[3]]
        if len(p) > 6:
            p[0].append(p[5])
        else:
            p[0].append(None)

    def p_mixin_guard(self, p):
        """ mixin_guard               : less_when mixin_guard_cond_list
        """
        p[0] = p[2]

    def p_mixin_guard_cond_list_aux(self, p):
        """ mixin_guard_cond_list    : mixin_guard_cond_list t_comma mixin_guard_cond
                                     | mixin_guard_cond_list less_and mixin_guard_cond
        """
        p[1].append(p[2])
        p[1].append(p[3])
        p[0] = p[1]

    def p_mixin_guard_cond_list(self, p):
        """ mixin_guard_cond_list     : mixin_guard_cond
        """
        p[0] = [p[1]]

    def p_mixin_guard_cond_rev(self, p):
        """ mixin_guard_cond          : less_not t_popen argument mixin_guard_cmp argument t_pclose
                                      | less_not t_popen argument t_pclose
        """
        p[0] = utility.reverse_guard(list(p)[3:-1])

    def p_mixin_guard_cond(self, p):
        """ mixin_guard_cond          : t_popen argument mixin_guard_cmp argument t_pclose
                                      | t_popen argument t_pclose
        """
        p[0] = list(p)[2:-1]

    def p_mixin_guard_cmp(self, p):
        """ mixin_guard_cmp           : '>'
                                      | '<'
                                      | '='
                                      | '>' '='
                                      | '=' '<'
        """
        p[0] = ''.join(list(p)[1:])

    def p_call_mixin(self, p):
        """ call_mixin                : identifier t_popen mixin_args_list t_pclose t_semicolon
        """
        p[1].parse(None)
        p[0] = Deferred(p[1], p[3], p.lineno(4))

    def p_mixin_args_arguments(self, p):
        """ mixin_args_list          : less_arguments
        """
        p[0] = [p[1]]

    def p_mixin_args_list_aux(self, p):
        """ mixin_args_list          : mixin_args_list t_comma mixin_args
                                     | mixin_args_list t_semicolon mixin_args
        """
        p[1].extend([p[3]])
        p[0] = p[1]

    def p_mixin_args_list(self, p):
        """ mixin_args_list          : mixin_args
        """
        p[0] = [p[1]]

    def p_mixin_args_aux(self, p):
        """ mixin_args                : mixin_args argument
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
        """ mixin_kwarg                : variable t_colon mixin_kwarg_arg_list
        """
        p[0] = Variable(list(p)[1:], p.lineno(2))

    def p_margument_list_aux(self, p):
        """ mixin_kwarg_arg_list       : mixin_kwarg_arg_list argument
        """
        p[1].extend(list(p)[2:])
        p[0] = p[1]

    def p_margument_list(self, p):
        """ mixin_kwarg_arg_list      : argument
        """
        p[0] = [p[1]]

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
                                       | import_statement
        """
        p[0] = p[1] if isinstance(p[1], list) else [p[1]]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_variable_decl(self, p):
        """ variable_decl            : variable t_colon style_list t_semicolon
        """
        p[0] = Variable(list(p)[1:-1], p.lineno(4))
        p[0].parse(self.scope)

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_property_decl(self, p):
        """ property_decl           : prop_open style_list t_semicolon
                                    | prop_open style_list css_important t_semicolon
                                    | prop_open empty t_semicolon
        """
        l = len(p)
        p[0] = Property(list(p)[1:-1], p.lineno(l - 1))

    def p_property_decl_arguments(self, p):
        """ property_decl           : prop_open less_arguments t_semicolon
        """
        p[0] = Property([p[1], [p[2]]], p.lineno(3))

    def p_prop_open_ie_hack(self, p):
        """ prop_open               : '*' prop_open
        """
        p[0] = (p[1][0], p[2][0])

    def p_prop_open(self, p):
        """ prop_open               : property t_colon
                                    | vendor_property t_colon
                                    | word t_colon
        """
        p[0] = p[1]

    def p_prop_open_interpolated(self, p):
        """ prop_open               : interpolated_property t_colon
        """
        p[0] = p[1]

    def p_interpolated_property(self, p):
        """ interpolated_property : interpolated_property_part
        """
        p[0] = [p[1]]

    def p_interpolated_property_aux(self, p):
        """ interpolated_property : interpolated_property interpolated_property_part
        """
        p[1].extend([p[2]])
        p[0] = p[1]

    def p_interpolated_property_part(self, p):
        """ interpolated_property_part  : variable_interpolated
                                        | css_property
                                        | css_vendor_property
                                        | '-'
        """
        p[0] = p[1]

    def p_interpolated_property_part_word(self, p):
        """ interpolated_property_part  : word
        """
        # Not sure whey word comes as a list.
        p[0] = p[1][0]


#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_style_list_aux(self, p):
        """ style_list              : style_list style
                                    | style_list t_comma style
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
                                    | string
                                    | word
                                    | property
                                    | vendor_property
                                    | estring
        """
        p[0] = p[1]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_identifier(self, p):
        """ identifier                : identifier_list
                                      | page
                                      | page filter
        """
        p[0] = Identifier(p[1], 0)

    def p_identifier_istr(self, p):
        """ identifier                : t_popen estring t_pclose
        """
        p[0] = Identifier(Call([p[2], p[3]]), 0)

    def p_identifier_list_aux(self, p):
        """ identifier_list           : identifier_list t_comma identifier_group
        """
        p[1].extend([p[2]])
        p[1].extend(p[3])
        p[0] = p[1]

    def p_identifier_list(self, p):
        """ identifier_list           : identifier_group
        """
        p[0] = p[1]

    def p_identifier_list_keyframe(self, p):
        """ identifier_list           : css_keyframes t_ws css_ident
                                      | css_keyframes t_ws css_ident t_ws
        """
        p[0] = list(p)[1:]

    def p_identifier_list_viewport(self, p):
        """ identifier_list           : css_viewport
                                      | css_viewport t_ws
        """
        p[0] = list(p)[1:]

    def p_identifier_group_op(self, p):
        """ identifier_group          : identifier_group child_selector ident_parts
                                      | identifier_group '+' ident_parts
                                      | identifier_group general_sibling_selector ident_parts
                                      | identifier_group '*'
        """
        p[1].extend([p[2]])
        if len(p) > 3:
            p[1].extend(p[3])
        p[0] = p[1]

    def p_identifier_group(self, p):
        """ identifier_group          : ident_parts
        """
        p[0] = p[1]

    def p_ident_parts_aux(self, p):
        """ ident_parts               : ident_parts ident_part
                                      | ident_parts filter_group
        """
        if isinstance(p[2], list):
            p[1].extend(p[2])
        else:
            p[1].append(p[2])
        p[0] = p[1]

    def p_ident_parts(self, p):
        """ ident_parts               : ident_part
                                      | selector
                                      | filter_group
                                      | variable_interpolated
        """
        if not isinstance(p[1], list):
            p[1] = [p[1]]
        p[0] = p[1]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_media_query_decl(self, p):
        """ media_query_decl            : css_media t_ws
                                        | css_media t_ws media_query_list
        """
        p[0] = list(p)[1:]

    def p_media_query_list_aux(self, p):
        """ media_query_list            : media_query_list t_comma media_query
        """
        p[0] = list(p)[1:]

    def p_media_query_list(self, p):
        """ media_query_list            : media_query
        """
        p[0] = [p[1]]

    def p_media_query_a(self, p):
        """ media_query                 : media_type
                                        | media_type media_query_expression_list
                                        | not media_type
                                        | not media_type media_query_expression_list
                                        | only media_type
                                        | only media_type media_query_expression_list
        """
        p[0] = list(p)[1:]

    def p_media_query_b(self, p):
        """ media_query                 : media_query_expression media_query_expression_list
                                        | media_query_expression
        """
        p[0] = list(p)[1:]

    def p_media_query_expression_list_aux(self, p):
        """ media_query_expression_list : media_query_expression_list and media_query_expression
                                        | and media_query_expression
        """
        p[0] = list(p)[1:]

    def p_media_query_expression(self, p):
        """ media_query_expression      : t_popen css_media_feature t_pclose
                                        | t_popen css_media_feature t_colon media_query_value t_pclose
        """
        p[0] = list(p)[1:]

    def p_media_query_value(self, p):
        """ media_query_value           : number
                                        | variable
                                        | word
                                        | color
                                        | expression
        """
        if utility.is_variable(p[1]):
            var = self.scope.variables(''.join(p[1]))
            if var:
                value = var.value[0]
                if hasattr(value, 'parse'):
                    p[1] = value.parse(self.scope)
                else:
                    p[1] = value
        if isinstance(p[1], Expression):
            p[0] = p[1].parse(self.scope)
        else:
            p[0] = p[1]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_selector(self, p):
        """ selector                  : '*'
                                      | '+'
                                      | child_selector
                                      | general_sibling_selector
        """
        p[0] = p[1]

    def p_ident_part(self, p):
        """ ident_part                : iclass
                                      | id
                                      | dom
                                      | combinator
                                      | color
                                      | word
        """
        # `word` is added to support TAG names containing dash characters.
        p[0] = p[1]

    def p_ident_part_aux(self, p):
        """ ident_part                : combinator vendor_property
        """
        p[0] = [p[1], p[2]]

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
                                      | css_filter t_ws
                                      | t_colon word
                                      | t_colon vendor_property
                                      | t_colon vendor_property t_ws
                                      | t_colon css_property
                                      | t_colon css_property t_ws
                                      | t_colon css_filter
                                      | t_colon css_filter t_ws
                                      | t_colon t_colon word
                                      | t_colon t_colon vendor_property
        """
        p[0] = list(p)[1:]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_ms_filter(self, p):
        """ ms_filter       : css_ms_filter
                            | css_ms_filter t_ws
        """
        p[0] = tuple(list(p)[1:])

    def p_fcall(self, p):
        """ fcall           : word t_popen argument_list t_pclose
                            | property t_popen argument_list t_pclose
                            | vendor_property t_popen argument_list t_pclose
                            | less_open_format argument_list t_pclose
                            | ms_filter t_popen argument_list t_pclose
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
                                | argument_list t_comma argument
        """
        p[1].extend(list(p)[2:])
        p[0] = p[1]

    def p_argument_list(self, p):
        """ argument_list       : argument
        """
        p[0] = [p[1]]

    def p_argument(self, p):
        """ argument        : expression
                            | string
                            | estring
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
                                    | fcall
        """
        p[0] = p[1]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_escaped_string(self, p):
        """ estring                 : t_eopen style_list t_eclose
                                    | t_eopen identifier_list t_eclose
        """
        p[0] = p[2]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_string_part(self, p):
        """ string_part             : variable_interpolated
                                    | css_string
        """
        p[0] = p[1]

    def p_string_part_list_aux(self, p):
        """ string_part_list        : string_part_list string_part
        """
        p[1].extend([p[2]])
        p[0] = p[1]

    def p_string_part_list(self, p):
        """ string_part_list        : string_part
        """
        p[0] = [p[1]]

    def p_string_aux(self, p):
        """ string                  : t_isopen string_part_list t_isclose
        """
        p[0] = ['"', p[2], '"']

    def p_string(self, p):
        """ string                  : css_string
        """
        p[0] = p[1]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_variable_neg(self, p):
        """ variable                : '-' variable
        """
        p[0] = ['-', p[2]]

    def p_variable_strange(self, p):
        """ variable                : t_popen variable t_pclose
        """
        p[0] = p[2]

    def p_variable(self, p):
        """ variable                : less_variable
                                    | less_variable t_ws
        """
#        p[0] = p[1]
        p[0] = tuple(list(p)[1:])

    def p_variable_interpolated(self, p):
        """ variable_interpolated  : less_variable_interpolated
                                   | less_variable_interpolated t_ws
        """
        p[0] = p[1]

    def p_color(self, p):
        """ color                   : css_color
                                    | css_color t_ws
        """
        try:
            p[0] = Color().fmt(p[1])
            if len(p) > 2:
                p[0] = [p[0], p[2]]
        except ValueError:
            value = 'Illegal color value `%s`' % p[1]
            self.error_reporter.warning(
                filename=self.target,
                line_no=p.lineno(1),
                value=value,
                )

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

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_class(self, p):
        """ class                     : css_class
                                      | css_class t_ws
        """
        p[0] = tuple(list(p)[1:])

    def p_interpolated_class_part(self, p):
        """ iclass_part               : less_variable
                                      | less_variable t_ws
                                      | class
        """
        p[0] = list(p)[1:]

    def p_interpolated_class_part_list_aux(self, p):
        """ iclass_part_list          : iclass_part_list iclass_part
        """
        p[1].extend([p[2]])
        p[0] = p[1]

    def p_interpolated_class_part_list(self, p):
        """ iclass_part_list          : iclass_part
        """
        p[0] = [p[1]]

    def p_interpolated_class(self, p):
        """ iclass                    : iclass_part_list
        """
        p[0] = p[1]

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_id(self, p):
        """ id                        : css_id
                                      | css_id t_ws
        """
        p[0] = tuple(list(p)[1:])

    def p_property(self, p):
        """ property                  : css_property
                                      | css_property t_ws
        """
        p[0] = (p[1],)

    def p_page(self, p):
        """ page                      : css_page
                                      | css_page t_ws
        """
        p[0] = tuple(list(p)[1:])

    def p_vendor_property(self, p):
        """ vendor_property           : css_vendor_property
                                      | css_vendor_property t_ws
        """
        p[0] = tuple(list(p)[1:])

    def p_media_type(self, p):
        """ media_type                : css_media_type
                                      | css_media_type t_ws
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
        """ general_sibling_selector  : t_tilde t_ws
                                      | t_tilde
        """
        p[0] = tuple(list(p)[1:])

    def p_scope_open(self, p):
        """ brace_open                : t_bopen
        """
        self.scope.push()
        p[0] = p[1]

    def p_scope_close(self, p):
        """ brace_close               : t_bclose
        """
        p[0] = p[1]

    def p_and(self, p):
        """ and                       : t_and t_ws
                                      | t_and
        """
        p[0] = tuple(list(p)[1:])

    def p_not(self, p):
        """ not                       : t_not t_ws
                                      | t_not
        """
        p[0] = tuple(list(p)[1:])

    def p_only(self, p):
        """ only                      : t_only t_ws
                                      | t_only
        """
        p[0] = tuple(list(p)[1:])

    def p_empty(self, p):
        'empty                        :'
        pass

#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

    def p_error(self, t):
        """ Internal error handler
        args:
            t (Lex token): Error token
        """
        if t:
            value = 'Syntax Error, token: `%s`, `%s`' % (t.type, t.value)
            self.error_reporter.error(
                filename=self.target,
                line_no=t.lineno,
                value=value,
                )

        while True:
            t = self.lex.token()
            if not t or t.value == '}':
                if len(self.scope) > 1:
                    self.scope.pop()
                break
        self.parser.restart()
        return t


class _DefaultErrorReporter(object):
    """
    A simple reporter which reports to standard error.
    """

    def error(self, filename, line_no, type, value):
        print("\x1b[31mE: %s line: %d, Syntax Error, token: `%s`, `%s`\x1b[0m"
              % (filename, line_no, type, value), file=sys.stderr)

    def warning(self, filename, line_no, value):
        print("\x1b[33mw: %s line: %d, Syntax Error, token: `%s`, `%s`\x1b[0m"
              % (filename, line_no, value), file=sys.stderr)
