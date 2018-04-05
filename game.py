# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:04:09 2018

@author: PG738LD
"""
from objects import Hand


class Gamestate:
    """A moment during a game that is calling decision from players.
    
    Parameters
    ----------
    hand_1 : Hand
        Hand of player 1
    hand_2 : Hand
        Hand of player 2
    source : int, 1 or 2
        1 for played card, 2 for openned card
    owner : int, 1 or 2
        The player who just played or openned
    turn : int, 1 or 2
        The player who is taking action right now
    table : list[Card]
        Cards played on discarded on the table
    pool : list[Card]
        Cards left in deck

    """
    def __init__(self, hand_1, hand_2, source, owner, turn, table, pool):
        self.hand_1 = hand_1
        self.hand_2 = hand_2
        self.source = source
        self.owner = owner
        self.turn = turn
        self.table = table
        self.pool = pool
    
    def next_(self, to_use):
        """Given a current scenario, the player decide to use the coming card
        or not to use it. Return the next scenario.
        """
        pass
    
    def pass_(self):
        """
        source   owner   turn   return
        1        1       1      n/a
        1        1       2      player 2 to open
        1        2       1      player 1 to open
        1        2       2      n/a
        2        1       1      player 2 to use
        2        1       2      player 2 to open
        2        2       1      player 1 to open
        2        2       2      player 1 to use
        """
        print("Player "+str(self.turn)+" said: Bu Yao!")
        if self.source == 1 or (self.source == 2 and self.owner != self.turn):
            print("Player "+str(self.turn)+" to open a new card...")
            new_card = self.pool[0]
            print("the new card is..."+new_card.hanzi)
            print("Let's assume nothing happens for the moment...")
            print("Player "+str(self.turn)+": Please make a decision now.")
            hand_1 = Hand(self.hand_1.private, self.hand_2.public, new_card)
            hand_2 = Hand(self.hand_2.private, self.hand_2.public, new_card)
            return Scenario(hand_1, hand_2, 2, self.turn, self.turn, 
                            self.table+[new_card], self.pool[1:])
        else:
            print("It's player "+str(3-self.turn)+"'s turn to make a decision")
            return Scenario(self.hand_1, self.hand_2, 2, self.owner, 
                            3 - self.turn, self.table, self.pool)
    
    def play_(self, order):
        #return Scenario()
        pass
    
    def use_(self, orders):
        pass
    
    
