"""
    LESSCPY Color functions
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import colorsys
from . import utility

class Color():
    def process(self, expression):
        """ Process color expression
            @param tuple: color expression
            @return: string
        """
        a, o, b = expression
        c1 = self._hextorgb(a)
        c2 = self._hextorgb(b)
        r = ['#']
        for i in range(3):
            v = self.operate(c1[i], c2[i], o)
            if v > 0xff: v = 0xff
            if v < 0: v = 0
            r.append("%02x" % v)
        return ''.join(r)
    
    def operate(self, a, b, o):
        """ Do operation on colors
            @param string: color
            @param string: color
            @param string: operator
        """
        operation = {
            '+': '__add__',
            '-': '__sub__',
            '*': '__mul__',
            '/': '__truediv__'
        }.get(o)
        v = getattr(a, operation)(b)
        return v
    
    def rgb(self, *args):
        """
        """
        if len(args) == 4:
            return self.rgba(*args)
        elif len(args) == 3:
            try:
                return self._rgbatohex(map(int, args))
            except ValueError:
                if all((a for a in args 
                        if a[-1] == '%' 
                        and 100 >= int(a[:-1]) >= 0)):
                    return self._rgbatohex([int(a[:-1]) * 255 / 100.0
                                            for a in args])
        raise ValueError('Illegal color values')
    
    def rgba(self, *args):
        """
        """
        if len(args) == 4:
            try:
                return self._rgbatohex(map(int, args))
            except ValueError:
                if all((a for a in args 
                        if a[-1] == '%' 
                        and 100 >= int(a[:-1]) >= 0)):
                    return self._rgbatohex([int(a[:-1]) * 255 / 100.0
                                            for a in args])
        raise ValueError('Illegal color values')
    
    def hsl(self, *args):
        """
        """
        if len(args) == 4:
            return self.hsla(*args)
        elif len(args) == 3:
            h, s, l = args
            if type(l) == str: l = int(l.strip('%'))
            if type(s) == str: s = int(s.strip('%'))
            rgb = colorsys.hls_to_rgb(int(h) / 360, l / 100, s / 100)
            color = (round(c * 255) for c in rgb)
            return self._rgbatohex(color)
        raise ValueError('Illegal color values')
    
    def hsla(self, *args):
        """
        """
        if len(args) == 4:
            h, s, l, a = args
            if type(l) == str: l = int(l.strip('%'))
            if type(s) == str: s = int(s.strip('%'))
            rgb = colorsys.hls_to_rgb(int(h) / 360, l / 100, s / 100)
            color = [round(c * 255) for c in rgb]
            color.append(round(float(a[:-1]) / 100.0, 2))
            return "rgba(%s,%s,%s,%s)" % tuple(color)
        raise ValueError('Illegal color values')
    
    def hue(self, *args):
        """
        """
        if args:
            h, l, s = self._hextohls(args[0])
            return round(h * 360, 3)
        raise ValueError('Illegal color values')
    
    def saturation(self, *args):
        """
        """
        if args:
            h, l, s = self._hextohls(args[0])
            return s * 100
        raise ValueError('Illegal color values')
    
    def lightness(self, *args):
        """
        """
        if args:
            h, l, s = self._hextohls(args[0])
            return l * 100
        raise ValueError('Illegal color values')
    
    def opacity(self, *args):
        """
        """
        pass
    
    def lighten(self, *args):
        """
        """
        if len(args) == 2:
            color, diff = args
            return self._ophsl(color, diff, 1, '__add__')
        raise ValueError('Illegal color values')
    
    def darken(self, *args):
        """
        """
        if len(args) == 2:
            color, diff = args
            return self._ophsl(color, diff, 1, '__sub__')
        raise ValueError('Illegal color values')
    
    def saturate(self, *args):
        """
        """
        if len(args) == 2:
            color, diff = args
            return self._ophsl(color, diff, 2, '__add__')
        raise ValueError('Illegal color values')
    
    def desaturate(self, *args):
        """
        """
        if len(args) == 2:
            color, diff = args
            return self._ophsl(color, diff, 2, '__sub__')
        raise ValueError('Illegal color values')
    
    def clamp(self, v):
        """
        """
        return min(1, max(0, v))
    
    def grayscale(self, *args):
        """
        Simply 100% desaturate.
        """
        if len(args) == 2:
            return self.desaturate(args[0], 100)
        raise ValueError('Illegal color values')

    def greyscale(self, *args):
        """
        Wrapper for grayscale
        """
        return self.grayscale(*args)
    
    def spin(self, *args):
        """
        """
        if len(args) == 2:
            color, deg = args
            if type(deg) == str: deg = int(deg.strip('%'))
            h, l, s = self._hextohls(color)
            h = ((h * 360) + deg) % 360
            h = 360 + h if h < 0 else h
            rgb = colorsys.hls_to_rgb(h / 360, l, s)
            color = (round(c * 255) for c in rgb)
            return self._rgbatohex(color)
        raise ValueError('Illegal color values')
    
    def mix(self, *args):
        """
        This algorithm factors in both the user-provided weight
        and the difference between the alpha values of the two colors
        to decide how to perform the weighted average of the two RGB values.
        
        It works by first normalizing both parameters to be within [-1, 1],
        where 1 indicates "only use color1", -1 indicates "only use color 0",
        and all values in between indicated a proportionately weighted average.
        
        Once we have the normalized variables w and a,
        we apply the formula (w + a)/(1 + w*a)
        to get the combined weight (in [-1, 1]) of color1.
        This formula has two especially nice properties:
        
         * When either w or a are -1 or 1, the combined weight is also that number
           (cases where w * a == -1 are undefined, and handled as a special case).
      
         * When a is 0, the combined weight is w, and vice versa
      
        Finally, the weight of color1 is renormalized to be within [0, 1]
        and the weight of color2 is given by 1 minus the weight of color1.
        
        Copyright (c) 2006-2009 Hampton Catlin, Nathan Weizenbaum, and Chris Eppstein
        http://sass-lang.com
        """
        if len(args) >= 2:
            try:
                c1, c2, w = args
            except ValueError:
                c1, c2 = args
                w = 50
            if type(w) == str: w = int(w.strip('%'))
            w = ((w / 100.0) * 2) - 1
            rgb1 = self._hextorgb(c1)
            rgb2 = self._hextorgb(c2)
            a = 0
            w1 = (((w if w * a == -1 else w + a) / (1 + w * a)) + 1)
            w1 = w1 / 2.0
            w2 = 1 - w1
            rgb = [
                rgb1[0] * w1 + rgb2[0] * w2,
                rgb1[1] * w1 + rgb2[1] * w2,
                rgb1[2] * w1 + rgb2[2] * w2,
            ]
            return self._rgbatohex(rgb)
        raise ValueError('Illegal color values')
        
    def fmt(self, color):
        """
            Format CSS Hex color code.
            uppercase becomes lowercase, 3 digit codes expand to 6 digit.
            @param string: color
        """
        if utility.is_color(color):
            color = color.lower().strip('#')
            if len(color) in [3, 4]:
                color = ''.join([c * 2 for c in color])
            return '#%s' % color
        raise ValueError('Cannot format non-color')
    
    def _rgbatohex(self, rgba):
        """
        """
        return '#%s' % ''.join(["%02x" % v for v in 
                                [0xff 
                                 if h > 0xff else 
                                 0 if h < 0 else h 
                                 for h in rgba]
                                ])
    def _hextorgb(self, hex):    
        """
        """
        hex = hex.strip()
        if hex[0] == '#':
            hex = hex.strip('#').strip(';')
            if len(hex) == 3:
                hex = [c * 2 for c in hex]
            else:
                hex = [hex[i:i+2] for i in range(0, len(hex), 2)]
            return tuple(int(c, 16) for c in hex)
        return [int(hex, 16)] * 3
        
    def _hextohls(self, hex):
        """
        """
        rgb = self._hextorgb(hex)
        return colorsys.rgb_to_hls(*[c / 255.0 for c in rgb])
    
    def _ophsl(self, color, diff, idx, op):
        """
        """
        if type(diff) == str: diff = int(diff.strip('%'))
        hls = list(self._hextohls(color))
        hls[idx] = self.clamp(getattr(hls[idx], op)(diff / 100))
        rgb = colorsys.hls_to_rgb(*hls)
        color = (round(c * 255) for c in rgb)
        return self._rgbatohex(color)
    
        
    
    