"""
    CSS Formatter class.
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
class Formatter(object):
    def format(self, parse, minify=False, xminify=False):
        """
        """
        eb = '\n' 
        if xminify:
            eb = ''
            minify = True
        self.minify = minify
        self.items = {}
        if minify:
            self.items.update({
                'nl': '',
                'tab': '',
                'ws': '',
                'eb': eb
            })
        else:
            self.items.update({
                'nl': '\n',
                'tab': '\t',
                'ws': ' ',
                'eb': eb
            })
        self.out = [u.format(self.items) 
                    for u in parse.result 
                    if u]
        return ''.join(self.out).strip()
        
    