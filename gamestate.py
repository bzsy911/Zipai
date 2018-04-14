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
    source : int, 1 or 2
        1 for played card, 2 for opened card
    owner : int, 1 or 2
        The player who just played or opened
    turn : int, 1 or 2
        The player who is on call right now
    table : (list[Card], list[Card])
        Cards played on discarded on the table
        0 for computer, 1 for human
    bench : Card or None
        The card being opened or played, waiting player to take usage of
    pool : Pool
        Cards left in deck

    """

    def __init__(self, game_info, hand_1, hand_2, source, owner, turn, table, bench, pool):
        self.game_info = game_info
        self.hand_1 = hand_1
        self.hand_2 = hand_2
        self.source = source
        self.owner = owner
        self.turn = turn
        self.table = table
        self.bench = bench
        self.pool = pool
        self.end = False

    def screen(self, pointing_pos=None):
        cpt_dealer = '[庄]' if self.game_info['dealer'] == 2 else ''
        hm_dealer = '[庄]' if self.game_info['dealer'] == 1 else ''

        cpt_private = '* ' * len(self.hand_2.private)
        cpt_public = ''

        hm_private = self.hand_1.display_private()
        hm_public = ''

        table_cpt = ''.join([x.hanzi for x in self.table[0]]) + ' ' * (43 - 2*len(self.table[0])) + '|'
        table_hm = ''.join([x.hanzi for x in self.table[1]]) + ' ' * (43 - 2*len(self.table[1])) + '|'

        bench_cpt = '  ' if (not self.bench or self.owner == 1) else self.bench.hanzi
        bench_hm = '  ' if (not self.bench or self.owner == 2) else self.bench.hanzi

        pointer = '  ' * pointing_pos + '^' if pointing_pos else ''

        screen = """
        Game: {round}
        
                       {cpt_name} {cpt_dealer}
        
           [{cpt_private}]
           [{cpt_public}]
         ______________________________________________
        |                                              |
        |   {table_cpt}
        |                     [{bench_cpt}]                     |
        |                     [{bench_hm}]                     |
        |   {table_hm}
        |______________________________________________|
                         Card Left: {left}
    
           [{hm_public}]
           [{hm_private}]
          {pointer}
                       {hm_name} {hm_dealer}
        """.format(round=self.game_info['round'],
                   cpt_name=self.game_info['cpt_name'],
                   cpt_dealer=cpt_dealer,
                   cpt_private=cpt_private,
                   cpt_public=cpt_public,
                   table_cpt=table_cpt,
                   bench_cpt=bench_cpt,
                   bench_hm=bench_hm,
                   table_hm=table_hm,
                   left=self.pool.left(),
                   hm_private=hm_private,
                   hm_public=hm_public,
                   pointer=pointer,
                   hm_name=self.game_info['hm_name'],
                   hm_dealer=hm_dealer)

        return screen

    def print_screen(self, pointing_pos=None):
        screen = self.screen(pointing_pos)
        Functions.stdout(screen)
        return

    def pick_left_right(self, length):
        self.print_screen(1)
        pos = 1
        while True:
            key_in = Functions.stdin()
            if key_in == 'enter' or key_in == 'space':
                return pos
            else:
                if pos > 1 and key_in == 'left':
                    pos -= 1
                elif pos < length and key_in == 'right':
                    pos += 1
            self.print_screen(pos)


class DealState(Gamestate):

    def __init__(self, game_info):
        self.dealer = game_info['dealer']
        hand_hm, hand_cpt, the_21, pool = DealState.deal(self.dealer)
        super().__init__(game_info, hand_hm, hand_cpt, 0, 0, self.dealer, ([], []), None, pool)
        self.log = self.get_log(the_21)

    @staticmethod
    def deal(dealer):
        pool = Pool()
        cards_1, cards_2 = pool.deal_hand(2)
        the_21 = pool.deal()
        if dealer == 1:
            cards_1.append(the_21)
        else:
            cards_2.append(the_21)
        hand_hm = Hand(cards_1, [])
        hand_cpt = Hand(cards_2, [])
        return hand_hm, hand_cpt, the_21, pool

    def get_log(self, the_21):
        dealer_name = self.game_info['hm_name'] if self.dealer == 1 else self.game_info['cpt_name']
        return """发牌完毕\n这把{dealer}做庄\n{dealer}摸的第21张牌是{the_21}""".format(dealer=dealer_name, the_21=the_21)

    def next_(self):
        # check if tian hu.
        # check Dia
        # draw cards if >= 3 Dia
        if self.dealer == 1:
            return HmPlayState(self.game_info, self.hand_1, self.hand_2,
                               self.source, self.owner, self.table, self.pool)
        else:
            return CptPlayState(self.game_info, self.hand_1, self.hand_2,
                                self.source, self.owner, self.table, self.pool)


class HmStrategyState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, owner, table, bench, pool):
        super().__init__(game_info, hand_1, hand_2, source, owner, 1, table, bench, pool)

    def pass_(self):
        _ = Functions.stdin()
        if self.owner == 1:
            return CptStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 1, self.table, self.bench, self.pool)
        else:
            self.table[0].append(self.bench)
            return HmOpenState(self.game_info, self.hand_1, self.hand_2, self.source, self.table, self.pool)

    def next_(self):
        return self.pass_()


class HmOpenState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, 2, 1, table, None, pool)

    def open_(self):
        _ = Functions.stdin()
        new_card = self.pool.deal()
        # check dia, xiao here, TBI
        # pass the card and just give it to hm
        return HmStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 1, self.table, new_card, self.pool)

    def next_(self):
        if self.pool.cards:
            return self.open_()
        else:
            return DrawGameState(self.game_info, self.hand_1, self.hand_2,
                                 self.source, 2, 1, self.table, None, self.pool)





class HmPlayState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, owner, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, owner, 1, table, None, pool)

    def play(self):
        pick_pos = self.pick_left_right(len(self.hand_1.private))
        played_card = self.hand_1.private.pop(pick_pos-1)
        return CptStrategyState(self.game_info, self.hand_1, self.hand_2, 1, 1, self.table, played_card, self.pool)

    def next_(self):
        return self.play()


class CptStrategyState(Gamestate):
    # make a decision of pass or use
    def __init__(self, game_info, hand_1, hand_2, source, owner, table, bench, pool):
        super().__init__(game_info, hand_1, hand_2, source, owner, 2, table, bench, pool)

    def pass_(self):
        if self.owner == 2:
            # must be opened by computer, turn to human to decide.
            return HmStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 2, self.table, self.bench, self.pool)
        else:
            # hm played or passed a card, go to pool and open
            self.table[1].append(self.bench)
            return CptOpenState(self.game_info, self.hand_1, self.hand_2, self.source, self.table, self.pool)

    def next_(self):
        return self.pass_()


class CptOpenState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, 1, 2, table, None, pool)

    def open_(self):
        new_card = self.pool.deal()
        # check dia, xiao here, TBI
        # pass the card and just give it to hm
        return CptStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 2, self.table, new_card, self.pool)

    def next_(self):
        if self.pool.cards:
            return self.open_()
        else:
            return DrawGameState(self.game_info, self.hand_1, self.hand_2,
                                 self.source, 1, 2, self.table, None, self.pool)


class CptPlayState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, owner, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, owner, 2, table, None, pool)

    def auto_play(self):
        played_card = self.hand_2.private.pop()
        return HmStrategyState(self.game_info, self.hand_1, self.hand_2, 1, 2, self.table, played_card, self.pool)

    def next_(self):
        return self.auto_play()


class DrawGameState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, owner, turn, table, bench, pool):
        super().__init__(game_info, hand_1, hand_2, source, owner, turn, table, bench, pool)
        self.end = True
