# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:04:09 2018

@author: PG738LD
"""

from gamestate import DealState


class Game:
    """Procedure of a Game:
    1. Deal - 发牌
    2. Mandatory Sets - 有Dia落地
    3. Dealer plays a card - 庄家出牌
    4. Used & Play OR Pass and Flip - 吃打或过翻
    5. Win or Draw - 胡牌或荒牌
    6. Scores - 分数
    """

    def __init__(self, dealer, user_info):
        # iterator of Gamestates
        # judge object
        # dealer: int, id of dealer
        # Human player's id is 1, Computer is 2.
        self.dealer = dealer
        self.game_info = user_info
        self.game_info['dealer'] = self.dealer
        self.states = []

    def __iter__(self):
        self.current_state = DealState(self.game_info)
        self.states.append(self.current_state)
        return self

    def __next__(self):
        self.current_state = self.current_state.next_()
        self.current_state.print_screen()
        self.states.append(self.current_state)
        if not self.current_state.pool.cards:
            raise StopIteration
        return

