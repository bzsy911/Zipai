# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 12:55:21 2018

@author: PG738LD
"""

import unittest
import objects as obj


class TestCardMethods(unittest.TestCase):

    def setUp(self):
        self.da2 = obj.Card(102)
        self.xiao6 = obj.Card(6)
        self.xiao10 = obj.Card(10)

    def test_attributes(self):
        self.assertEqual(self.da2.num, 2)
        self.assertEqual(self.da2.tp, True)
        self.assertEqual(self.da2.red, True)
        self.assertEqual(self.xiao6.num, 6)
        self.assertEqual(self.xiao6.tp, False)
        self.assertEqual(self.xiao6.red, False)

    def test_str(self):
        self.assertEqual(self.da2.__str__(), '贰')
        self.assertEqual(self.xiao10.__str__(), '十')

    def test_lt(self):
        ls = [self.da2, self.xiao10, self.xiao6]
        self.assertEqual(sorted(ls), [self.xiao6, self.xiao10, self.da2])


class TestPairMethods(unittest.TestCase):
    
    def setUp(self):
        self.pair = obj.Pair(107)
    
    def test_attributes(self):
        self.assertEqual(self.pair.orders, [107, 107])
        self.assertEqual(self.pair.red, 2)
        self.assertEqual(self.pair.points, 0)
    
    
class TestShunMethods(unittest.TestCase):
    pass
class TestYiErSanMethods(unittest.TestCase):
    pass
class TestMixedMethods(unittest.TestCase):
    pass
class TestErQiShiMethods(unittest.TestCase):
    pass
class TestXiaoMethods(unittest.TestCase):
    pass
class TestBengMethods(unittest.TestCase):
    pass
class TestDiaMethods(unittest.TestCase):
    pass
class TestPaoMethods(unittest.TestCase):
    pass
class TestDandiaoMethods(unittest.TestCase):
    pass
class TestPaShunMethods(unittest.TestCase):
    pass
class TestPaMixedMethods(unittest.TestCase):
    pass
class TestPa2710Methods(unittest.TestCase):
    pass
class TestLiangjiaMethods(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()