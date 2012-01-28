"""
    CSS Formatter class.
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
class Formatter(object):
    def format(self, parse, minify=False, xminify=False):
        """ Format css output from parser
            @param Parse-result object: Parse-result object
            @param bool: Minify flag
            @param bool: Skip end of block newlines
            @return: string
        """
        eb = '\n' 
        if xminify:
            eb = ''
            minify = True
        self.items = {}
        if minify:
            self.items.update({
                'nl': '',
                'tab': '',
                'ws': '',
                'endblock': eb
            })
        else:
            self.items.update({
                'nl': '\n',
                'tab': '\t',
                'ws': ' ',
                'endblock': eb
            })
        self.out = []
        if parse.result:
            for u in parse.result:
                self.out.extend(self.fprint(u))
        return ''.join(self.out)
                
    def fprint(self, node):
        """ Format node.
            @param Node object: Node object
        """
        out = []
        if not node: return out
        if 'proplist' in node.parsed:
            node.parsed['proplist'] = ''.join([self.sprintf(p.format, p.parsed)
                                               for p in node.parsed['proplist']
                                               if p])
            if node.parsed['proplist']:
                out.append(self.sprintf(node.format, node.parsed))
        else:
            out.append(self.sprintf(node.format, node.parsed))
        if 'inner' in node.parsed:
            if node._blocktype:
                out.append(self.fblockinner(node))
            else:
                for iu in node.parsed['inner']:
                    out.extend(self.fprint(iu))
        return out
    
    def fblockinner(self, node):
        """ Format inner block type
            @param Node: node
            @return: str
        """
        sub = []
        for iu in node.parsed['inner']:
            sub.extend(self.fprint(iu))
        sub = ''.join(sub)
        if sub:
            if self.items['tab']:
                sub = '\t'+''.join(sub)
                sub = sub.replace('\n', '\n\t').rstrip('\t')
            node.parsed['proplist'] = sub  
            return self.sprintf(node.format, node.parsed)
        return ''
                
    def sprintf(self, frm, items):
        """ Perform format action
            @param string: Format string
            @param dict: format items
            @return: string
        """
        items.update(self.items)
        return frm % items
