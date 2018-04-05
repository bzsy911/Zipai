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
    
    def setUp(self):
        self.shun234 = obj.Shun(3)
        self.shun456 = obj.Shun(105)
    
    def test_attributes(self):
        self.assertEqual(self.shun234.orders, [2, 3, 4])
        self.assertEqual(self.shun234.red, 1)
        self.assertEqual(self.shun234.points, 0)
        self.assertEqual(self.shun456.orders, [104, 105, 106])
        self.assertEqual(self.shun456.red, 0)
        self.assertEqual(self.shun456.points, 0)
 
    
class TestYiErSanMethods(unittest.TestCase):
    
    def setUp(self):
        self.Da123 = obj.YiErSan(1)
        self.Xiao123 = obj.YiErSan(0)
    
    def test_attributes(self):
        self.assertEqual(self.Da123.orders, [101, 102, 103])
        self.assertEqual(self.Xiao123.orders, [1, 2, 3])
        self.assertEqual(self.Xiao123.__str__(), '[一二三]')
        self.assertEqual(self.Da123.red, 1)
        self.assertEqual(self.Xiao123.red, 1)
        self.assertEqual(self.Da123.points, 6)
        self.assertEqual(self.Xiao123.points, 3)
        
        
class TestMixedMethods(unittest.TestCase):
    
    def setUp(self):
        self.mixedDoubleDa1 = obj.Mixed(1, 1)
        self.mixedDoubleXiao1 = obj.Mixed(1, 0)
    
    def test_attributes(self):
        self.assertEqual(self.mixedDoubleDa1.orders, [1, 101, 101])
        self.assertEqual(self.mixedDoubleXiao1.orders, [1, 1, 101])
        self.assertEqual(self.mixedDoubleDa1.red, 0)
        self.assertEqual(self.mixedDoubleXiao1.red, 0)
        self.assertEqual(self.mixedDoubleDa1.points, 0)
        self.assertEqual(self.mixedDoubleXiao1.points, 0)
 
       
class TestErQiShiMethods(unittest.TestCase):
    
    def setUp(self):
        self.Da2710 = obj.ErQiShi(1)
        self.Xiao2710 = obj.ErQiShi(0)
    
    def test_attributes(self):
        self.assertEqual(self.Da2710.orders, [102, 107, 110])
        self.assertEqual(self.Xiao2710.orders, [2, 7, 10])
        self.assertEqual(self.Da2710.red, 3)
        self.assertEqual(self.Xiao2710.red, 3)
        self.assertEqual(self.Da2710.points, 6)
        self.assertEqual(self.Xiao2710.points, 3)
           
    
class TestXiaoMethods(unittest.TestCase):
    
    def setUp(self):
        self.xiao3 = obj.Xiao(3)
        self.xiao107 = obj.Xiao(107)
    
    def test_attributes(self):
        self.assertEqual(self.xiao3.orders, [3, 3, 3])
        self.assertEqual(self.xiao3.red, 0)
        self.assertEqual(self.xiao3.points, 3)
        self.assertEqual(self.xiao107.orders, [107, 107, 107])
        self.assertEqual(self.xiao107.red, 3)
        self.assertEqual(self.xiao107.points, 6)
 
    def test_gang(self):
        gang3_1 = self.xiao3.gang(1)
        gang3_0 = self.xiao3.gang(0)
        gang107_1 = self.xiao107.gang(1)
        gang107_0 = self.xiao107.gang(0)      
        self.assertEqual(gang3_1.points, 9) 
        self.assertEqual(gang3_0.points, 6)
        self.assertEqual(gang3_1.orders, [3, 3, 3, 3])
        self.assertEqual(gang3_0.orders, [3, 3, 3, 3])   
        self.assertEqual(gang3_1.red, 0)  
        self.assertEqual(gang3_0.red, 0)             
        self.assertEqual(gang107_1.points, 12) 
        self.assertEqual(gang107_0.points, 9)
        self.assertEqual(gang107_1.orders, [107, 107, 107, 107])
        self.assertEqual(gang107_0.orders, [107, 107, 107, 107])   
        self.assertEqual(gang107_1.red, 4)  
        self.assertEqual(gang107_0.red, 4)
    
    def test_dia(self):
        dia3 = self.xiao3.dia()
        dia107 = self.xiao107.dia()       
        self.assertEqual(dia3.points, 9)
        self.assertEqual(dia3.red, 0)
        self.assertEqual(dia3.orders, [3, 3, 3, 3])
        self.assertEqual(dia107.points, 12)
        self.assertEqual(dia107.red, 4)
        self.assertEqual(dia107.orders, [107, 107, 107, 107])
        
    def test_pao(self):
        pao3 = self.xiao3.pao()
        pao107 = self.xiao107.pao()
        self.assertEqual(pao3.orders, [3, 3, 3, 3])
        self.assertEqual(pao3.red, 0)
        self.assertEqual(pao3.points, 6)
        self.assertEqual(pao107.orders, [107, 107, 107, 107])
        self.assertEqual(pao107.red, 4)
        self.assertEqual(pao107.points, 9)
                
        
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
class TestHandMethods(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()