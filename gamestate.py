# -*- coding: utf-8 -*-
"""
Created on Fri Apr  13 00:58:09 2018

@author: PG738LD
"""

from const import Functions
from objects import Hand, Pool


class Gamestate:
    """A moment during a game that is calling action from players.

    Parameters
    ----------
    hand_1 : Hand
        Hand of player 1
    hand_2 : Hand
        Hand of player 2
    type : str
        "deal", "hm_strategy", "cpt_strategy", "hm_open", "cpt_open"
        "hm_play", "cpt_play", "hm_pass", "cpt_pass", ...
    source : int, 1 or 2
        1 for played card, 2 for opened card
    owner : int, 1 or 2
        The player who just played or opened
    turn : int, 1 or 2
        The player who is on call right now
    table : (list[Card], list[Card])
        Cards played on discarded on the table
        0 for computer, 1 for human
    pool : Pool
        Cards left in deck

    """

    def __init__(self, game_info, hand_1, hand_2, source, owner, turn, table, pool):
        self.game_info = game_info
        self.hand_1 = hand_1
        self.hand_2 = hand_2
        self.source = source
        self.owner = owner
        self.turn = turn
        self.table = table
        self.pool = pool

    def screen(self, pointing_pos=None):
        cpt_dealer = '[庄]' if self.game_info['dealer'] == 2 else ''
        hm_dealer = '[庄]' if self.game_info['dealer'] == 1 else ''

        cpt_private = '* ' * 20
        cpt_coming = '' if self.turn == 1 else ' {coming}'.format(coming=self.hand_2.coming.hanzi)
        cpt_public = ''

        hm_private = self.hand_1.display_private()
        hm_public = ''
        hm_coming = '' if self.turn == 2 else ' {coming}'.format(coming=self.hand_1.coming.hanzi)

        table_cpt = ''.join([x.hanzi for x in self.table[0]]) + ' ' * (43 - 2*len(self.table[0])) + '|'
        table_hm = ''.join([x.hanzi for x in self.table[1]]) + ' ' * (43 - 2*len(self.table[1])) + '|'

        pointer = '  ' * pointing_pos + '^' if pointing_pos else ''

        screen = """
        Game: {round}
        
                       {cpt_name} {cpt_dealer}
        
           [{cpt_private}{cpt_coming}]
           [{cpt_public}]
         ______________________________________________
        |                                              |
        |   {table_cpt}
        |                                              |
        |                                              |
        |   {table_hm}
        |______________________________________________|
                         Card Left: {left}
    
           [{hm_public}]
           [{hm_private}{hm_coming}]
          {pointer}
                       {hm_name} {hm_dealer}
        """.format(round=self.game_info['round'],
                   cpt_name=self.game_info['cpt_name'],
                   cpt_dealer=cpt_dealer,
                   cpt_private=cpt_private,
                   cpt_coming=cpt_coming,
                   cpt_public=cpt_public,
                   table_cpt=table_cpt,
                   table_hm=table_hm,
                   left=self.pool.left(),
                   hm_private=hm_private,
                   hm_public=hm_public,
                   hm_coming=hm_coming,
                   pointer=pointer,
                   hm_name=self.game_info['hm_name'],
                   hm_dealer=hm_dealer)

        return screen

    def print_screen(self, pointing_pos=None):
        screen = self.screen(pointing_pos)
        Functions.stdout(screen)
        return

    def pick_left_right(self, pos, length):
        # on mac left = 68, right = 67, enter = 10, space = 32
        self.print_screen(pos)
        while True:
            key_in = Functions.stdin()
            if key_in == 'enter' or key_in == 'space':
                return pos
            else:
                if pos > 1 and key_in == 'left':
                    pos -= 1
                    if pos == 21:
                        pos -= 1
                elif pos < length and key_in == 'right':
                    pos += 1
                    if pos == 21:
                        pos += 1
            self.print_screen(pos)


class DealState(Gamestate):

    def __init__(self, game_info):
        hand_hm, hand_cpt, pool = DealState.deal()
        self.dealer = game_info['dealer']
        super().__init__(game_info, hand_hm, hand_cpt, 0, 0, self.dealer, ([], []), pool)

    @staticmethod
    def deal():
        pool = Pool()
        cards_1, cards_2 = pool.deal_hand(2)
        the_21 = pool.deal()
        hand_hm = Hand(cards_1, [], the_21)
        hand_cpt = Hand(cards_2, [], the_21)
        return hand_hm, hand_cpt, pool

    def next_(self):
        # check if tian hu.
        # check Dia
        # draw cards if >= 3 Dia
        if self.dealer == 1:
            return HmStrategyState(self.game_info, self.hand_1, self.hand_2, self.source, self.owner, self.table, self.pool, True)
        else:
            return CptStrategyState(self.game_info, self.hand_1, self.hand_2, self.source, self.owner, self.table, self.pool, True)


class HmStrategyState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, owner, table, pool, initial_play=False):
        super().__init__(game_info, hand_1, hand_2, source, owner, 1, table, pool)
        self.initial_play = initial_play

    def play_21(self):
        # hm first play as dealer
        pick_pos = self.pick_left_right(1, 21)
        if pick_pos < 21:
            played_card = self.hand_1.private.pop(pick_pos-1)
            hand_hm = Hand(self.hand_1.private + [self.hand_1.coming], [], played_card)
        else:
            played_card = self.hand_1.coming
            hand_hm = self.hand_1
        hand_cpt = self.hand_2.replace_coming(played_card)
        return CptStrategyState(self.game_info, hand_hm, hand_cpt, 1, 1, ([], [played_card]), self.pool)

    def pass_(self):
        if self.owner == 1:
            return CptStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 1, self.table, self.pool)
        else:
            return HmOpenState(self.game_info, self.hand_1, self.hand_2, self.source, self.table, self.pool)

    def next_(self):
        if self.initial_play:
            return self.play_21()
        else:
            return self.pass_()


class HmOpenState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, 2, 1, table, pool)

    def open_(self):
        _ = Functions.stdin()
        new_card = self.pool.deal()
        # check dia, xiao here, TBI
        # pass the card and just give it to hm
        hand_hm = self.hand_1.replace_coming(new_card)
        hand_cpt = self.hand_2.replace_coming(new_card)
        table_hm = self.table[1] + [new_card]
        return HmStrategyState(self.game_info, hand_hm, hand_cpt, 2, 1, (self.table[0], table_hm), self.pool)

    def next_(self):
        return self.open_()


class CptStrategyState(Gamestate):
    # make a decision of pass or use
    def __init__(self, game_info, hand_1, hand_2, source, owner, table, pool, initial_play=False):
        super().__init__(game_info, hand_1, hand_2, source, owner, 2, table, pool)
        self.initial_play = initial_play

    def auto_play_21(self):
        # for temporary using only
        key_in = Functions.stdin()
        played_card = self.hand_2.coming
        hand_hm = self.hand_1.replace_coming(played_card)
        return HmStrategyState(self.game_info, hand_hm, self.hand_2, 1, 2, ([played_card], []), self.pool)

    def pass_(self):
        if self.owner == 2:
            # must be opened by computer, turn to human to decide.
            return HmStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 2, self.table, self.pool)
        else:
            # hm played or passed a card, go to pool and open
            return CptOpenState(self.game_info, self.hand_1, self.hand_2, self.source, self.table, self.pool)

    def next_(self):
        if self.initial_play:
            return self.auto_play_21()
        else:
            return self.pass_()


class CptOpenState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, 1, 2, table, pool)

    def open_(self):
        new_card = self.pool.deal()
        # check dia, xiao here, TBI
        # pass the card and just give it to hm
        hand_hm = self.hand_1.replace_coming(new_card)
        hand_cpt = self.hand_2.replace_coming(new_card)
        table_cpt = self.table[0] + [new_card]
        return CptStrategyState(self.game_info, hand_hm, hand_cpt, 2, 2, (table_cpt, self.table[1]), self.pool)

    def next_(self):
        return self.open_()
