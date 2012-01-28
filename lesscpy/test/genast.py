import sys, re
sys.path.append('..')
import lesscpy.lessc.parser

m = []

with open('../lessc/parser.py') as f:
    for l in f.readlines():
        r = re.findall('def[ \t]+(p_[a-z_0-9]+)([^\(]*)', l)
        if r: m.append(r[0][0])
        
p = lesscpy.lessc.parser.LessParser

for u in m:
    if u == 'p_error': continue
    print(getattr(p, u).__doc__)