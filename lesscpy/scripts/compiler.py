"""
    CSS/LESSCSS run script

    http://lesscss.org/#docs
    
    Copyright (c)
    See LICENSE for details
    <jtm@robot.is>
"""
import os
import sys
import glob
import argparse
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from lesscpy.lessc import parser
from lesscpy.lessc import lexer
from lesscpy.lessc import formatter
#
#    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
def run():
    aparse = argparse.ArgumentParser(description='LessCss Compiler', epilog='<< jtm@robot.is @_o >>')
    aparse.add_argument('-I', '--include', action="store", type=str,
                        help="Included less-files (comma separated)")
    aparse.add_argument('-x', '--minify', action="store_true", 
                        default=False, help="Minify output")
    aparse.add_argument('-X', '--xminify', action="store_true", 
                        default=False, help="Minify output, no end of block newlines")
    aparse.add_argument('-m', '--min-ending', action="store_true", 
                        default=False, help="Add '.min' into output filename. eg, name.min.css")
    aparse.add_argument('-D', '--dry-run', action="store_true", 
                        default=False, help="Dry run, do not write files")
    aparse.add_argument('-v', '--verbose', action="store_true", 
                        default=False, help="Verbose mode")
    aparse.add_argument('-o', '--out', action="store", help="Output directory")
    group = aparse.add_argument_group('Debugging')
    group.add_argument('-S', '--scopemap', action="store_true", 
                        default=False, help="Scopemap")
    group.add_argument('-V', '--debug', action="store_true", 
                        default=False, help="Debug mode")
    group.add_argument('-L', '--lex-only', action="store_true", 
                        default=False, help="Run lexer on target")
    group.add_argument('-N', '--no-css', action="store_true", 
                        default=False, help="No css output")
    aparse.add_argument('target', help="less file or directory")
    args = aparse.parse_args()
    #
    #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    if args.lex_only:
        lex = lexer.LessLexer()
        ll = lex.file(args.target)
        while True:
            tok = ll.token()
            if not tok: break
            print(tok)
        print('EOF')
        sys.exit()
    #
    #    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 
    yacctab = 'yacctab' if args.debug else None
    scope = None
    if args.include:
        for u in args.include.split(','):
            if args.debug: print("compiling include: %s" % u)
            p = parser.LessParser(
                                  yacc_debug=False,
                                  lex_optimize=True,
                                  yacc_optimize=True,
                                  yacctab=yacctab)
            p.parse(filename=u, debuglevel=0)
            if not scope:
                scope = p.scope
            else:
                scope[0].update(p.scope[0])
    else:
        scope = None
    p = None
    f = formatter.Formatter()
    if not os.path.exists(args.target):
        sys.exit("Target not found '%s' ..." % args.target)
    if os.path.isdir(args.target):
        if not args.out:
            sys.exit("Compile directory option needs -o ...")
        elif os.path.isdir(args.out) and not os.listdir(args.out) == []: 
            sys.exit("Output directory not empty...")
        else:
            if not os.path.isdir(args.out):
                if args.verbose:
                    print("Creating '%s'" % args.out)
                if not args.dry_run:
                    os.mkdir(args.out)
        less = glob.glob(os.path.join(args.target, '*.less'))
        for lf in less:
            outf = os.path.splitext(os.path.basename(lf))
            min = '.min' if args.min_ending else ''
            outf = "%s/%s%s.css" % (args.out, outf[0], min) 
            if args.verbose: print("%s -> %s" % (lf, outf))
            
            p = parser.LessParser(yacc_debug=False,
                                  lex_optimize=True,
                                  yacc_optimize=True,
                                  scope=scope,
                                  yacctab=yacctab)
            p.parse(filename=lf, debuglevel=0)
            css = f.format(p, args.minify, args.xminify)
            if not args.dry_run:
                with open(outf, 'w') as outfile:
                    outfile.write(css)
        if args.dry_run:
            print('Dry run, nothing done.')
            
    else:
        if args.verbose: print("compiling target: %s" % args.target)
        p = parser.LessParser(yacc_debug=(args.debug),
                              lex_optimize=True,
                              yacc_optimize=(not args.debug),
                              scope=scope)
        p.parse(filename=args.target, debuglevel=0)
        if args.scopemap:
            args.no_css = True
            p.scopemap()
        if not args.no_css and p:
            out = f.format(p, args.minify, args.xminify)
            print(out)
    