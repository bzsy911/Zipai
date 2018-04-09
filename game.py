# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:04:09 2018

@author: PG738LD
"""
from objects import Hand, Pool


class Game:
    """Procedure of a Game:
    1. Deal - 发牌
    2. Mandatory Sets - 有Dia落地
    3. Dealer plays a card - 庄家出牌
    4. Used & Play OR Pass and Flip - 吃打或过翻
    5. Win or Draw - 胡牌或荒牌
    6. Scores - 分数
    """

    def __init__(self, dealer):
        # list of Gamestates
        # judge object
        # dealer: int, id of dealer
        # Human player's id is 1, Computer is 2.
        self.dealer = dealer
        self.states = [self.deal_state()]
        self.winner = 2 - self.dealer

    def deal_state(self):
        pool = Pool()
        cards_1, cards_2 = pool.deal_hand(2)
        the_21 = pool.deal()

        hand_hm = Hand(cards_1, [], the_21)
        hand_cpt = Hand(cards_2, [], the_21)

        state = Gamestate(hand_hm, hand_cpt, 0, 0, self.dealer, [], pool)


    def current_state(self):
        return self.states[-1]
    
    def screen(self):
        return self.current_state().screen()
        

class Gamestate:
    """A moment during a game that is calling decision from players.
    
    Parameters
    ----------
    hand_1 : Hand
        Hand of player 1
    hand_2 : Hand
        Hand of player 2
    source : int, 1 or 2
        1 for played card, 2 for opened card
    owner : int, 1 or 2
        The player who just played or opened
    turn : int, 1 or 2
        The player who is taking action right now
    table : list[Card]
        Cards played on discarded on the table
    pool : Pool
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

    def screen(self):
        cpt_name = 'Stella'
        cpt_private = '*' * 20
        cpt_21 = '' if self.turn == 1 else ' {the_21}'.format(the_21=self.hand_2.coming.hanzi)
        cpt_public = ''

        hm_private = self.hand_1.display_private()
        hm_coming = '' if self.turn == 2 else ' {the_21}'.format(the_21=self.hand_1.coming.hanzi)
        hm_name = 'Guest'

        return """
    {cpt_name}
    [{cpt_private}{cpt_21}]
    [{cpt_public}]
     _________________________
    |                         |
    |                         |
    |                         |
    |                         |
    |_________________________|
          Card Left: {left}
    
    []
    [{hm_private}{hm_coming}]
    {hm_name}
    """.format(cpt_name=cpt_name,
               cpt_private=cpt_private,
               cpt_21=cpt_21,
               cpt_public=cpt_public,
               left=self.pool.left(),
               hm_private=hm_private,
               hm_coming=hm_coming,
               hm_name=hm_name)

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
            new_card = self.pool.deal()
            print("the new card is..."+new_card.hanzi)
            print("Let's assume nothing happens for the moment...")
            print("Player "+str(self.turn)+": Please make a decision now.")
            hand_1 = Hand(self.hand_1.private, self.hand_2.public, new_card)
            hand_2 = Hand(self.hand_2.private, self.hand_2.public, new_card)
            return Gamestate(hand_1, hand_2, 2, self.turn, self.turn,
                             self.table+[new_card], self.pool)
        else:
            print("It's player "+str(3-self.turn)+"'s turn to make a decision")
            return Gamestate(self.hand_1, self.hand_2, 2, self.owner,
                             3 - self.turn, self.table, self.pool)
    
    def play_(self, order):
        # return Gamestate()
        pass
    
    def use_(self, orders):
        pass

