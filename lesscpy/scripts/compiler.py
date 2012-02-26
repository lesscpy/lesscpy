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

def ldirectory(inpath, outpath, args, scope):
    """
    """
    yacctab = 'yacctab' if args.debug else None
    if not outpath:
        sys.exit("Compile directory option needs -o ...")
    else:
        if not os.path.isdir(outpath):
            if args.verbose:
                print("Creating '%s'" % outpath)
            if not args.dry_run:
                os.mkdir(outpath)
    less = glob.glob(os.path.join(inpath, '*.less'))
    f = formatter.Formatter()
    for lf in less:
        outf = os.path.splitext(os.path.basename(lf))
        minx = '.min' if args.min_ending else ''
        outf = "%s/%s%s.css" % (outpath, outf[0], minx) 
        if not args.force and os.path.exists(outf):
            recompile = os.path.getmtime(outf) < os.path.getmtime(lf)
        else: 
            recompile = True
        if recompile:
            if args.verbose: print("%s -> %s" % (lf, outf))
            p = parser.LessParser(yacc_debug=False,
                                  lex_optimize=True,
                                  yacc_optimize=True,
                                  scope=scope,
                                  yacctab=yacctab,
                                  verbose=args.verbose)
            p.parse(filename=lf, debuglevel=0)
            css = f.format(p, args.minify, args.xminify)
            if not args.dry_run:
                with open(outf, 'w') as outfile:
                    outfile.write(css)
        elif args.verbose: print('skipping %s, not modified' % lf)
    if args.recurse:
        [ldirectory(os.path.join(inpath, name), os.path.join(outpath, name), args, scope) 
         for name in os.listdir(inpath) 
         if os.path.isdir(os.path.join(inpath, name))
         and not name.startswith('.')
         and not name == outpath]
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
    aparse.add_argument('-v', '--verbose', action="store_true", 
                        default=False, help="Verbose mode")
    dgroup = aparse.add_argument_group('Directory options', 
                                       'Compiles all *.less files in directory that '
                                       'have a newer timestamp than it\'s css file.')
    dgroup.add_argument('-o', '--out', action="store", help="Output directory")
    dgroup.add_argument('-r', '--recurse', action="store_true", help="Recursive into subdirectorys")
    dgroup.add_argument('-f', '--force', action="store_true", help="Force recompile on all files")
    dgroup.add_argument('-m', '--min-ending', action="store_true", 
                        default=False, help="Add '.min' into output filename. eg, name.min.css")
    dgroup.add_argument('-D', '--dry-run', action="store_true", 
                        default=False, help="Dry run, do not write files")
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
            p = parser.LessParser(
                                  yacc_debug=False,
                                  lex_optimize=True,
                                  yacc_optimize=True,
                                  yacctab=yacctab,
                                  verbose=args.verbose)
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
        ldirectory(args.target, args.out, args, scope)     
        if args.dry_run:
            print('Dry run, nothing done.')  
    else:
        p = parser.LessParser(yacc_debug=(args.debug),
                              lex_optimize=True,
                              yacc_optimize=(not args.debug),
                              scope=scope,
                              verbose=args.verbose)
        p.parse(filename=args.target, debuglevel=0)
        if args.scopemap:
            args.no_css = True
            p.scopemap()
        if not args.no_css and p:
            out = f.format(p, args.minify, args.xminify)
            print(out)
    