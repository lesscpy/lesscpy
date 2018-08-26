"""
    lesscpy color tests.
"""
import unittest

from lesscpy.lessc import color


class TestLessColor(unittest.TestCase):
    def setUp(self):
        self.color = color.Color()

    def test_rgb(self):
        test = self.color.rgb
        for r, g, b, v in [
            (255, 255, 255, '#ffffff'),
            (100, 100, 100, '#646464'),
            (0, 0, 0, '#000000'),
            ('70%', '70%', '70%', '#b2b2b2'),
            ('1%', '1%', '1%', '#020202'),
            ('100%', '100%', '100%', '#ffffff'),
            ('0%', '0%', '0%', '#000000'),
        ]:
            self.assertEqual(test(r, g, b), v)
        for r, g, b, a, v in [
            (255, 255, 255, 0.5, '#ffffff'),
            (100, 100, 100, 0.9, '#646464'),
            (0, 0, 0, 100, '#000000'),
        ]:
            self.assertEqual(test(r, g, b, a), v)
        for args in [
            (255, 255, 256),
            (0, -1, 0),
            ('100%', '100%', 200),
            ('100%', '100%', '200%'),
        ]:
            self.assertRaises(ValueError, test, args)

    def test_rgba(self):
        test = self.color.rgba
        for r, g, b, a, v in [
            (255, 255, 255, 255, '#ffffff'),
            (100, 100, 100, 100, '#646464'),
            (0, 0, 0, 0, 'rgba(0,0,0,0)'),
            ('70%', '70%', '70%', '70%', '#b2b2b2b2'),
            ('1%', '1%', '1%', '1%', '#02020202'),
            ('100%', '100%', '100%', '100%', '#ffffffff'),
            ('0%', '0%', '0%', '0%', 'rgba(0,0,0,0)'),
        ]:
            self.assertEqual(test(r, g, b, a), v)
        for args in [
            (255, 255, 255, 256),
            (0, 0, 0, -1),
            ('100%', '100%', '100%', 200),
            ('100%', '100%', '100%', '200%'),
        ]:
            self.assertRaises(ValueError, test, args)

    def test_argb(self):
        test = self.color.argb
        for a, r, g, b, v in [
            (255, 255, 255, 255, '#ffffffff'),
            (100, 100, 100, 100, '#ff646464'),
            (0, 0, 0, 0, '#00000000'),
            ('70%', '70%', '70%', '70%', '#b2b2b2b2'),
            ('1%', '1%', '1%', '1%', '#02020202'),
            ('100%', '100%', '100%', '100%', '#ffffffff'),
            ('0%', '0%', '0%', '0%', '#00000000'),
        ]:
            self.assertEqual(test(a, r, g, b), v)
        for args in [
            (255, 255, 255, 256),
            (-1, 0, 0, 0),
            (200, '100%', '100%', '100%'),
            ('200%', '100%', '100%', '100%'),
        ]:
            self.assertRaises(ValueError, test, args)

    def test_hsl(self):
        """
        """
        test = self.color.hsl
        for h, s, l, v in [
            (31, '1%', '4%', '#0a0a0a'),
            (0, '100%', '100%', '#ffffff'),
            (100, '100%', '100%', '#ffffff'),
            (0, '0%', '0%', '#000000'),
            (100, '0%', '0%', '#000000'),
        ]:
            self.assertEqual(test(h, s, l), v)

    def test_hsla(self):
        test = self.color.hsla
        for h, s, l, a, v in [
            (31, '1%', '4%', '0%', 'rgba(10.0,10.0,10.0,0.0)'),
            (31, '30%', '4%', '1%', 'rgba(13.0,10.0,7.0,0.01)'),
            (31, '60%', '4%', '20%', 'rgba(16.0,10.0,4.0,0.2)'),
            (31, '90%', '4%', '60%', 'rgba(19.0,11.0,1.0,0.6)'),
            (31, '100%', '4%', '100%', 'rgba(20.0,11.0,0.0,1.0)'),
        ]:
            self.assertEqual(test(h, s, l, a), v)

    def test_fmt(self):
        test = self.color.fmt
        self.assertEqual(test('#000'), '#000000')
        self.assertEqual(test('#000000'), '#000000')
        self.assertEqual(test('#0000'), '#00000000')
        self.assertEqual(test('#00000000'), '#00000000')
        self.assertEqual(test('#AAA'), '#aaaaaa')
        self.assertEqual(test('#Abc'), '#aabbcc')
        self.assertEqual(test('#AbCdEf'), '#abcdef')
        self.assertRaises(ValueError, test, '#xxx')
        self.assertRaises(ValueError, test, None)
        self.assertRaises(ValueError, test, 'aabbcc')
        self.assertRaises(ValueError, test, '#4aabbcc')

    def test_saturate(self):
        test = self.color.saturate
        for c, p, v in [
            ('#555', '1%', '#565454'),
            ('#555', '10%', '#5e4c4c'),
            ('#555', '20%', '#664444'),
            ('#555', '40%', '#773333'),
            ('#555', '60%', '#882222'),
            ('#555', '100%', '#aa0000'),
            ('#000', '100%', '#000000'),
            ('#000', '0%', '#000000'),
            ('#fff', '100%', '#ffffff'),
            ('#fff', '0%', '#ffffff'),
            ('#29332f', '1%', '#29332f'),
            ('#29332f', '10%', '#243830'),
            ('#29332f', '20%', '#203c31'),
            ('#29332f', '40%', '#174533'),
            ('#29332f', '60%', '#0d4f35'),
            ('#29332f', '100%', '#005c37'),
        ]:
            self.assertEqual(test(c, p), v, v)

    def test_desaturate(self):
        test = self.color.desaturate
        for c, p, v in [
            ('#555', '1%', '#555555'),
            ('#555', '10%', '#555555'),
            ('#555', '20%', '#555555'),
            ('#555', '40%', '#555555'),
            ('#555', '60%', '#555555'),
            ('#555', '100%', '#555555'),
            ('#000', '100%', '#000000'),
            ('#000', '0%', '#000000'),
            ('#fff', '100%', '#ffffff'),
            ('#fff', '0%', '#ffffff'),
            ('#29332f', '1%', '#29332f'),
            ('#29332f', '10%', '#2e2e2e'),
            ('#29332f', '20%', '#2e2e2e'),
            ('#29332f', '40%', '#2e2e2e'),
            ('#29332f', '60%', '#2e2e2e'),
            ('#29332f', '100%', '#2e2e2e'),
        ]:
            self.assertEqual(test(c, p), v, v)

    def test_spin(self):
        test = self.color.spin
        for c, p, v in [
            ('#555', '1%', '#555555'),
            ('#555', '10%', '#555555'),
            ('#555', '20%', '#555555'),
            ('#555', '40%', '#555555'),
            ('#555', '60%', '#555555'),
            ('#555', '100%', '#555555'),
            ('#000', '100%', '#000000'),
            ('#000', '0%', '#000000'),
            ('#fff', '100%', '#ffffff'),
            ('#fff', '0%', '#ffffff'),
            ('#29332f', '1%', '#29332f'),
            ('#29332f', '10%', '#293331'),
            ('#29332f', '20%', '#293332'),
            ('#29332f', '40%', '#293033'),
            ('#29332f', '60%', '#292d33'),
            ('#29332f', '100%', '#2c2933'),
        ]:
            self.assertEqual(test(c, p), v, v)
