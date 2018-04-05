# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:15:29 2018

@author: PG738LD
"""

"""############################################################
   # Card     Set              Partial                        #
   #          |-- Pair         |-- Dandiao                    #
   # Hand     |-- Shun         |-- PaShun                     #
   #          |-- YiErSan      |-- PaMixed                    #
   #          |-- Mixed        |-- Pa2710                     #
   #          |-- ErQiShi      |-- Liangjia                   #
   #          |-- Ke                                          #
   #          |   |-- Xiao                                    #
   #          |   |-- Beng                                    #
   #          |-- Gang                                        #
   #              |-- Dia                                     #
   #              |-- Pao                                     #
   ############################################################
"""

from const import HANZI, Functions

from collections import deque


class Card:
    """A card is defined by 2 features, its number and type.
    
    Parameters
    ----------
    order : int
        An integer in range(1, 11) or range(101, 111).
    
    Attributes
    ----------
    num : int
        The playing number of this card.
    tp : boolean
        True means capital card; False means little card.
    red : boolean
        Card is defined to be red if its number is either 2, 7, or 10, 
        otherwise it is black.
    hanzi : str
        The number of this card appeared on the real game card.
    """
    
    def __init__(self, order):
        self.order = order
        self.num = self.order % 100
        self.tp = bool(self.order // 100)
        self.red = True if self.num in [2, 7, 10] else False
        self.hanzi = HANZI[self.order]
        
    def __str__(self):
        return self.hanzi
    
    def __lt__(self, other):
        return self.order < other.order



class Set:
    """A (valid) Set is a group of 2, 3, or 4 cards that is allowed to appear
    (as a group) in a winning hand. Types of Sets are Pair, Shun(normal, 123),
    Mixed, 2710, Ke(Xiao, Beng), Gang(Dia, Pao).    
    
    Parameters
    ----------
    orders : list[int]
        Orders to initialize cards
    qia : int, Optional (default == -1)
        1,2,3,4 for qia-position, 0 for not-qia, -1 for unknown
    
    Attributes
    ----------
    cards : list[Card]
    length : int
    red : int
        Number of red cards
    points : int
    """
    
    def __init__(self, orders, qia=-1):
        self.orders = sorted(orders)
        self.qia = qia
        self.cards = [Card(x) for x in self.orders]
        self.length = len(self.orders)
        self.red = len([c for c in self.cards if c.red])
        self.points = 0
    
    def __str__(self):
        if self.qia < 1:
            return ''.join(['['] + [x.__str__() for x in self.cards] + [']'])
        else:
            return ''.join(
                    ['['] + 
                    [self.cards[i].__str__() for i in range(self.length) if i+1 != self.qia] + 
                    ['+'] + 
                    [self.cards[self.qia-1].__str__()] + 
                    [']']
                    )


class Pair(Set):
    """Just a pair.
    
    Parameters
    ----------
    order : int
        The order of any card in this pairs
    qia : int, Optional (default == -1)
        2 for diandiao, 0 for zimo, -1 for unknown
    """
    def __init__(self, order, qia=-1):
        super().__init__([order]*2, qia)


class Shun(Set):
    """A length 3 set that contains consecutive numbers from 234 to 8910. 
    
    Parameters
    ----------
    mid : int
        The middle order of this Shun, from 3 to 9, or 103 to 109
    qia : int, Optional (default == -1)
        1,2,3 for qia-position, 0 for not-qia, -1 for unknown
    """
    def __init__(self, mid, qia=-1):
        super().__init__([mid-1, mid, mid+1], qia)


class YiErSan(Shun):
    """A special Shun [1,2,3].
    
    Parameters
    ----------
    tp : boolean
        True means capital 123, False means little 123.
    qia : int, Optional (default == -1)
        1,2,3 for qia-position, 0 for not-qia, -1 for unknown
    """
    def __init__(self, tp, qia=-1):
        super().__init__(2+100*tp, qia)
        self.points = 3 + 3*tp


class Mixed(Set):
    """A length 3 set that contains a single number but mixed types.
    
    Parameters
    ----------
    num : int
        The number of this Mixed, from 1 to 10
    two_caps : boolean
        The number of capitals, True for 2, False for 1
    qia : int, Optional (default == -1)
        1,3 for qia-position, 0 for not-qia, -1 for unknown
    """
    def __init__(self, num, two_caps, qia=-1):
        super().__init__([num, num+100*two_caps, num+100], qia)


class ErQiShi(Set):
    """A special Set [2, 7, 10].
    
    Parameters
    ----------
    tp : boolean
        True means capital 2710, False means little 2710.
    qia : int, Optional (default == -1)
        1,2,3 for qia-position, 0 for not-qia, -1 for unknown
    """
    def __init__(self, tp, qia=-1):
        super().__init__([x+100*tp for x in [2, 7, 10]], qia)
        self.points = 3 + 3*tp


class Ke(Set):
    """A Set that contains 3 identical cards.
    
    Parameters
    ----------
    order : int
        The order of any card in this Ke.
    qia : int, Optional (default == -1)
        3 for beng, 0 for xiao, -1 for unknown
    """
    def __init__(self, order, qia=-1):
        super().__init__([order]*3, qia)
    
    def gang(self):
        return Gang(self.orders[0])
        

class Xiao(Ke):
    """A special Ke that qia == 0.
    
    Parameters
    ----------
    order : int
        The order of any card in this Xiao.
    """
    def __init__(self, order):
        super().__init__(order, 0)
        self.points = 3 + 3*(order//100)
    
    def gang(self, zimo=False):
        if zimo:
            return Dia(self.orders[0])
        else:
            return Pao(self.orders[0], 1)
        
    def dia(self):
        return self.gang(True)
    
    def pao(self):
        return self.gang()
    

class Beng(Ke):
    """A special Ke that qia > 0.
    
    Parameters
    ----------
    order : int
        The order of any card in this Beng
    """
    def __init__(self, order):
        super().__init__(order, 3)
        self.points = 1 + 2*(order//100)
    
    def gang(self, zimo=False):
        return Pao(self.orders[0], 2-1*zimo)
    
    def pao(self):
        return self.gang()


class Gang(Set):
    """A Set that contains 4 identical cards.
    
    Parameters
    ----------
    order : int
        The order of any card in this Gang
    qia : int, Optional (default == -1)
        3, 4 for pao, 0 for dia, -1 for unknown
    """
    def __init__(self, order, qia=-1):
        super().__init__([order]*4, qia)


class Dia(Gang):
    """A special Gang that qia == 0
    
    Parameters
    ----------
    order : int
        The order of any card in this Dia
    """
    def __init__(self, order):
        super().__init__(order, 0)
        self.points = 9 + 3*(order//100)


class Pao(Gang):
    """A special Gang that qia > 0
    
    Parameters
    ----------
    order : int
        The order of any card in this Dia.
    num_zimo : int
        Number of Zimo Card in this Pao, 1 or 2
    """
    def __init__(self, order, num_zimo):
        super().__init__(order, 4-num_zimo)
        self.points = 6 + 3*(order//100)
    
    def __str__(self):
        if self.qia == 3:
            return super().__str__()
        else:
            return ('[' + self.cards[0].__str__()*2 + '+' + 
                      self.cards[0].__str__()*2 + ']')



class Partial:
    """A Partial is a group of 1 or 2 cards that is calling for a card to
    become a Set. Types of Partials are Dandiao, Liangjia, PartialShun(normal, 123),
    Mixed, Partial2710.    
    
    Parameters
    ----------
    orders : list[int]
        Orders to initialize cards
    
    Attributes
    ----------
    cards : list[Card]
    length : int
    red : int
        Number of red cards
    
    """
    def __init__(self, orders):
        self.orders = sorted(orders)
        self.cards = [Card(x) for x in self.orders]
        self.length = len(self.orders)
        self.red = len([c for c in self.cards if c.red])
    
    def __str__(self):
        return ''.join(['['] + [x.__str__() for x in self.cards] + [']'])
    
    def qia(self, last):
        return Set(self.orders+[last], self.length+1)


class Dandiao(Partial):
    """Just a single card.
    
    Parameters
    ----------
    order : int
        The order of this card
    """    
    def __init__(self, order):
        super().__init__([order])
    
    def fu(self):
        return Pair(self.orders[0], 2)
        

class Liangjia(Partial):
    """Two identical cards holding in hand.
    
    Parameters
    ----------
    order : int
        The order of any of this 2 cards
    """  
    def __init__(self, order):
        super().__init__([order]*2)
    
    def xiao(self):
        return Xiao(self.orders[0])
    
    def beng(self):
        return Beng(self.orders[0])
    
    def qia(self):
        return Mixed(self.cards[0].num, 
                     self.cards[0].tp, 
                     1 if self.cards[0].tp else 3)



class PaShun(Partial):
    """Two different cards holding in hand, waiting for the third.
    
    Parameters
    ----------
    orders : list[int]
        The orders of the 2 cards of this PaShun
    
    Attributes
    ----------
    is_lian : boolean
        True if 2 numbers are adjacent, False if separate
    waiting_list : list[int]
        The candidate card orders of the third
    
    """  
    def __init__(self, orders):
        super().__init__(orders)
        self.is_lian = self.orders[1]-self.orders[0]==1
        self.waiting_list = [self.orders[0]+1] if not self.is_lian else \
        [x for x in [self.orders[0]-1, self.orders[1]+1] if x%100 in range(1,11)]

    def qia(self):
        if not self.is_lian:
            return self.qia_ka()
        elif len(self.waiting_list) == 1:
            return self.qia_bian(self.waiting_list[0])
        else:
            third = input('which card to qia? '+str(self.waiting_list[0])+
                          ' or '+str(self.waiting_list[1])+'\n')
            return self.qia_bian(int(third))
    
    def qia_ka(self):
        return Shun(self.cards[0].order+1, 2) if self.cards[0].num!=1 else \
        YiErSan(self.cards[0].tp, 2)
    
    def qia_bian(self, third):
        if third > self.cards[1].order:
            return Shun(self.cards[1].order, 3) if third%100!=3 else \
            YiErSan(self.cards[0].tp, 3)
        else:
            return Shun(self.cards[0].order, 1) if third%100!=1 else \
            YiErSan(self.cards[0].tp, 1)


class PaMixed(Partial):
    """Two cards with same number but different types.
    
    Parameters
    ----------
    num : int
        The number of this PaMixed
    """
    def __init__(self, num):
        super().__init__([num, num+100])
    
    def qia(self, tp):
        return Mixed(self.cards[0].num, tp, 2)


class Pa2710(Partial):
    """Two of 2, 7, and 10, waiting the third.
    
    Parameters
    ----------
    orders : list[int]
        The orders of the 2 cards of this Partial
    
    Attributes
    ----------
    waiting_list : list[int]
        The candidate number of the third
    """
    def __init__(self, orders):
        super().__init__(orders)
        self.waiting_list = [x+100*self.cards[0].tp for x in [2,7,10] if \
                             x not in [n%100 for n in orders]]
    
    def qia(self):
        return ErQiShi(self.cards[0].tp, (self.waiting_list[0] % 100)//5+1)


class Hand:
    """The basic setup of a playing hand, including private cards holding in 
    hand, public sets placed on table, and the coming card triggering events.
    
    Parameters
    ----------
    private : list[Card]
        Cards holding in hand
    public : list[Set]
        Sets placed on table
    coming : Card
        The new card taken from card pool, or played from hand, by a player
    
    Attributes
    ----------
    orders : list[int]
        The corresponding orders of private cards
    dups_holding : int
        Number of same cards as coming holding in hand privately
    private_usage : list[Set]
        List of possiblities of using the coming card, all possiblities are 
        considered, regardless of rules
    public_usage : [int] (current inconsistent with private_usage here)
        The index in public of the Set that can pao(dia) the coming card
    shout : TBD
        The corresponding slang to shout out after decision
    """
    def __init__(self, private, public, coming):
        self.private = sorted(private)
        self.public = public
        self.coming = coming
        self.orders = [x.order for x in self.private]
        self.dups_holding = self.orders.count(self.coming.order)
        self.private_usage = self.check_private()
        self.public_usage = self.check_public()
        self.shout = self.shout()
        

    def check_public(self):
        for i in range(len(self.public)):
            if [x.order for x in self.public[i]].count(self.coming.order) == 3:
                return i
        return []

    def check_private(self):
        res = []
        for cat in ['gang', 'ke', 'shun', '2710', 'mixed']:
            res += getattr(self, '_check_'+cat)()
        return res
    
    def _check_gang(self):
        return [Gang(self.coming.order)] if self.dups_holding == 3 else []
    
    def _check_ke(self):
        return [Ke(self.coming.order)] if self.dups_holding == 2 else []

    def _check_shun(self):
        res = []
        # check left, two-sides, and right respectively
        pos = [-2, -1, 1, 2]
        for i in range(3):
            if (self.coming.order + pos[i] in self.orders and 
                self.coming.order + pos[i+1] in self.orders):
                if self.coming.num == 3-i:
                    res.append(YiErSan(self.coming.tp))
                else:
                    res.append(Shun(self.coming.order + i - 1))
        return res
    
    def _check_2710(self):
        if self.coming.num in [2, 7, 10]:
            the_other_two = [x.order for x in ErQiShi(self.coming.tp).cards]
            the_other_two.remove(self.coming.order)
            if set(the_other_two) <= set(self.orders):
                return [ErQiShi(self.coming.tp)]
        return []
            
    def _check_mixed(self):
        # two ways to qia mixed
        res = []
        if set([self.coming.num, self.coming.num+100]) <= set(self.orders):
            res.append(Mixed(self.coming.num, self.coming.tp))
        if self.orders.count(self.coming.order-(2*self.coming.tp-1)*100) == 2:
            res.append(Mixed(self.coming.num, not self.coming.tp))
        return res
    
    def shout(self):
        pass
    
    def group(self):
        # aim to list all posible combinations of private card
        # assume: no dia is in private. They should be dropped as soon as appear
        # rules: Xiaos must be grouped 
        # if length == 3k, make 0 pair, 0 dandiao
        # if length == 3k+1, make 1 pair, or 1 dandiao
        # if length == 3k+2, make 1 pair, 0 dandiao
        xiaos = set([order for order in self.orders if self.orders.count(order) == 3])
        d = [order for order in self.orders if order not in xiaos]
        
        # search with bfs, keep a dict of strs to avoid dup
        groupings = set()
        queue = deque([([],d)])
        
        while queue:
            node = queue.popleft()
            
                
        
if __name__=='__main__':
    
    import random
    
    def shuffle():
        deck = []
        for i in range(10):
            deck.extend([Card(i+1), Card(i+101)] * 4)
        random.shuffle(deck)
        return deck
    
    deck = shuffle()
    h = Hand(sorted(deck[:20]), [], deck[20])
    print([c.hanzi for c in h.private])
    print(h.coming.hanzi)
    print([res.__str__() for res in h.private_usage])
