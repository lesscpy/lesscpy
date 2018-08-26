import unittest

import lesscpy.lessc.utility as utility


class TestUtility(unittest.TestCase):
    def test_analyze(self):
        test = utility.analyze_number
        self.assertEqual((0, ''), test('0'))
        self.assertEqual((1, ''), test('1'))
        self.assertEqual(type(test('1')[0]), int)
        self.assertEqual(type(test('-1')[0]), int)
        self.assertEqual((1.0, ''), test('1.0'))
        self.assertEqual(type(test('-1.0')[0]), float)
        self.assertEqual((0, 'px'), test('0px'))
        self.assertEqual((1, 'px'), test('1px'))
        self.assertEqual((1.0, 'px'), test('1.0px'))
        self.assertEqual((0, 'px'), test('-0px'))
        self.assertEqual((-1, 'px'), test('-1px'))
        self.assertEqual(type(test('-1px')[0]), int)
        self.assertEqual((-1.0, 'px'), test('-1.0px'))
        self.assertEqual(type(test('-1.0px')[0]), float)
        self.assertRaises(SyntaxError, test, 'gg')
        self.assertRaises(SyntaxError, test, '-o')
        self.assertRaises(SyntaxError, test, '')

    def test_split_unit(self):
        test = utility.split_unit
        self.assertEqual(('', ''), test(None))
        self.assertEqual(('', ''), test(False))
        self.assertEqual(('', ''), test('qwerty'))
        self.assertEqual(('1', ''), test(1))
        self.assertEqual(('1', ''), test('1'))
        self.assertEqual(('1', 'px'), test('1px'))
        self.assertEqual(('-1', 'px'), test('-1px'))

    def test_is_int(self):
        test = utility.is_int
        self.assertTrue(test(1))
        self.assertTrue(test('1'))
        self.assertTrue(test('-1'))
        self.assertTrue(test(-1))
        self.assertFalse(test(False))
        self.assertFalse(test(None))
        self.assertFalse(test(0.0))

    def test_is_float(self):
        test = utility.is_float
        self.assertFalse(test(1))
        self.assertFalse(test('1'))
        self.assertFalse(test(False))
        self.assertFalse(test(None))
        self.assertTrue(test(0.0))
        self.assertTrue(test(-0.0))
        self.assertTrue(test('77.0565'))
        self.assertTrue(test('-0.0'))

    def test_is_color(self):
        test = utility.is_color
        self.assertTrue(test('#123'))
        self.assertTrue(test('#123456'))
        self.assertTrue(test('#Df3'))
        self.assertTrue(test('#AbCdEf'))
        self.assertFalse(test('#AbCdEg'))
        self.assertFalse(test('#h12345'))
        self.assertFalse(test('#12345'))
        self.assertFalse(test('AbCdEf'))
        self.assertFalse(test(''))
        self.assertFalse(test('.925'))
        self.assertFalse(test(False))
        self.assertFalse(test([]))

    def test_is_variable(self):
        test = utility.is_variable
        self.assertTrue(test('@var'))
        self.assertTrue(test('-@var'))
        self.assertFalse(test('var'))
        self.assertFalse(test(''))
        self.assertFalse(test(False))
        self.assertFalse(test([]))

    def test_with_unit(self):
        test = utility.with_unit
        self.assertEqual('1px', test((1, 'px')))
        self.assertEqual('1px', test(1, 'px'))
        self.assertEqual('1.0px', test(1.0, 'px'))
        self.assertEqual('0.0px', test('.0', 'px'))
        self.assertEqual('0.6px', test(.6, 'px'))
        self.assertEqual('1', test(1))
        self.assertEqual('1', test(1, None))
        self.assertEqual('1', test(1, ))

    def test_convergent_round(self):
        test = utility.convergent_round
        self.assertEqual(-4, test(-4.5))
        self.assertEqual(-4, test(-3.5))
        self.assertEqual(-2, test(-2.5))
        self.assertEqual(-2, test(-1.5))
        self.assertEqual(0, test(-0.5))
        self.assertEqual(0, test(0.5))
        self.assertEqual(2, test(1.5))
        self.assertEqual(2, test(2.5))
        self.assertEqual(3.0, test(10.0 / 3, 0))
        self.assertEqual(4, test(3.5))
        self.assertEqual(4, test(4.5))
