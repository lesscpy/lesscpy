"""
    LESSCPY Color functions
    
    Copyright (c)
    See LICENSE for details.
    <jtm@robot.is>
"""
import colorsys

class LessColor():
    def process(self, expression):
        """ Process color expression
            @param tuple: color expression
            @return: string
        """
        a, o, b = expression
        c1 = self.hex_to_rgb(a)
        c2 = self.hex_to_rgb(b)
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
    
    def rgb(self, r, g, b):
        """ RGB color function
            @param str: RED channel
            @param str: GREEN channel
            @param str: BLUE channel
            @return: str
        """
        return self.__str_rgb((int(r), int(g), int(b)))
    
    def hex_to_rgb(self, hex, *args):
        """ Convert HEX color code to rgb
            @param str: hex code 
            @return tuple
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
    
    def hex_to_hls(self, hex, *args):
        """ Convert Hex color code to hls
            @param str: hex code 
            @return tuple
        """
        rgb = self.hex_to_rgb(hex)
        return colorsys.rgb_to_hls(*[c / 255.0 for c in rgb])
    
    def hls(self, h, l, s, *args):
        """
            Create HEX color value from hls
            @param h: hue (0 <= h <= 360)
            @param l: lightness (0 <= l <= 100)
            @param s: saturation (0 <= l <= 100)
        """
        if type(l) == str: l = int(l.strip('%'))
        if type(s) == str: s = int(s.strip('%'))
        rgb = colorsys.hls_to_rgb(int(h) / 360, l / 100, s / 100)
        return self.__format_rgb(rgb)
    
    def hsl(self, h, s, l, *args):
        """
            Wrapper for hls
        """
        return self.hls(h, l, s)
    
    def hue(self, color, *args):
        """
            Returns the hue channel of color
            @param str: hex code 
            @return int
        """
        h, l, s = self.hex_to_hls(color)
        return round(h * 360, 3)
    
    def saturation(self, color, *args):
        """
            Returns the saturation channel of color
            @param str: hex code 
            @return int
        """
        h, l, s = self.hex_to_hls(color)
        return round(s * 100)
    
    def lightness(self, color, *args):
        """
            Returns the lightness channel of color
            @param str: hex code 
            @return int
        """
        h, l, s = self.hex_to_hls(color)
        return round(l * 100)
    
    def saturate(self, color, p, *args):
        """
        """
        if type(p) == str: p = int(p.strip('%'))
        h, l, s = self.hex_to_hls(color)
        rgb = colorsys.hls_to_rgb(h, l, s + (p / 100))
        return self.__format_rgb(rgb)
    
    def desaturate(self, color, p, *args):
        """
        """
        if type(p) == str: p = int(p.strip('%'))
        h, l, s = self.hex_to_hls(color)
        rgb = colorsys.hls_to_rgb(h, l, s - (p / 100))
        return self.__format_rgb(rgb)
    
    def lighten(self, color, p, *args):
        """
        """
        if type(p) == str: p = int(p.strip('%'))
        h, l, s = self.hex_to_hls(color)
        rgb = colorsys.hls_to_rgb(h, l + (p / 100), s)
        return self.__format_rgb(rgb)
    
    def darken(self, color, p, *args):
        """
        """
        if type(p) == str: p = int(p.strip('%'))
        h, l, s = self.hex_to_hls(color)
        rgb = colorsys.hls_to_rgb(h, l - (p / 100), s)
        return self.__format_rgb(rgb)
    
    def greyscale(self, color, *args):
        """
        """
        return self.desaturate(color, 100)
    
    def fadein(self, color, pc, *args):
        """
        """
        pass
    
    def fadeout(self, color, pc, *args):
        """
        """
        pass
    
    def fade(self):
        """
        """
        pass
    
    def spin(self, color, deg):
        """
        """
        if type(deg) == str: deg = int(deg.strip('%'))
        h, l, s = self.hex_to_hls(color)
        h = ((h * 360) + deg) % 360
        h = 360 + h if h < 0 else h
        rgb = colorsys.hls_to_rgb(h / 360, l, s)
        return self.__format_rgb(rgb)
    
    def mix(self, color1, color2, weight):
        """
        """
        pass
    
    def format(self, color):
        """
            Format CSS Hex color code.
            uppercase becomes lowercase, 3 digit codes expand to 6 digit.
            @param string: color
        """
        if type(color) == str and color[0] == '#':
            color = color.lower().strip().strip('#').strip(';')
            if len(color) == 3:
                color = ''.join([c * 2 for c in color])
            return '#%s' % color
        raise ValueError('Cannot format non-color')
    
    def __format_rgb(self, rgb):
        """ Format RGB tuple to string
            @param tuple: RGB tuple
            @return: string
        """
        color = (round(c * 255) for c in rgb)
        return self.__str_rgb(color)
        
    def __str_rgb(self, rgb):
        """
        """
        return '#%s' % ''.join(["%02x" % v for v in 
                                [0xff 
                                 if h > 0xff else 
                                 0 if h < 0 else h 
                                 for h in rgb]
                                ])
    
    