"""
    lesscpy tests.
"""
import unittest
from lesscpy.lessc import color


class TestLessColor(unittest.TestCase):
    def setUp(self):
        self.color = color.LessColor()
        
    def test_hls(self):
        self.assertEqual('#bf406a', self.color.hls(340, 50, 50))
        self.assertEqual('#bf8040', self.color.hls(30, 50, 50))
        self.assertEqual('#bf406a', self.color.hls('340', '50%', '50%'))
        self.assertEqual('#bf8040', self.color.hls('30', '50%', '50%'))
        
    def test_hue(self):
        pass
    
    def test_saturation(self):
        pass
    
    def test_lightness(self):
        pass
    
    def test_alpha(self):
        pass
    
    def test_saturate(self):
        self.assertEqual('#203c31', self.color.saturate('#29332f', 20))
    
    def test_desaturate(self):
        self.assertEqual('#29332f', self.color.desaturate('#203c31', 20))
    
    def test_lighten(self):
        self.assertEqual('#ffcccc', self.color.lighten('#f00', 40))
    
    def test_darken(self):
        self.assertEqual('#330000', self.color.darken('#f00', 40))
    
    def test_greyscale(self):
        return
        self.assertEqual('#2e2e2e', self.color.greyscale('#203c31'))
    
    def test_fadein(self):
        pass
    
    def test_fadeout(self):
        pass
    
    def test_fade(self):
        pass
    
    def test_spin(self):
        self.assertEqual('#bf6b40', self.color.spin('#bf406a', 40))
        self.assertEqual('#bf4055', self.color.spin('#bf8040', -40))
    
    def test_mix(self):
        pass
        
if __name__ == '__main__':
    unittest.main()