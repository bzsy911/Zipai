# -*- coding: utf-8 -*-
"""
Created on Fri Apr  13 00:58:09 2018

@author: PG738LD
"""

from const import Functions, HANZI, ACTIONS
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

    def screen(self, pointing_actions=None, action_choices=None, qia_choices=None, pointing_cards=None):
        cpt_dealer = '[庄]' if self.game_info['dealer'] == 2 else ''
        hm_dealer = '[庄]' if self.game_info['dealer'] == 1 else ''

        cpt_private = '* ' * (len(self.hand_2.private[0]*3) + len(self.hand_2.private[1]))
        cpt_public = self.hand_2.display_public()

        hm_private = self.hand_1.display_private()
        hm_public = self.hand_1.display_public()
        # hm_private = self.hand_1.orders
        # hm_public = self.hand_1.public

        table_cpt = ''.join([x.hanzi for x in self.table[0]]) + ' ' * (43 - 2*len(self.table[0])) + '|'
        table_hm = ''.join([x.hanzi for x in self.table[1]]) + ' ' * (43 - 2*len(self.table[1])) + '|'

        bench_cpt = '  ' if (not self.bench or self.owner == 1) else self.bench.hanzi
        bench_hm = '  ' if (not self.bench or self.owner == 2) else self.bench.hanzi

        if action_choices:
            padding_1 = ' ' * 22
            action_icons = ''.join([HANZI[ACTIONS[i]] for i in action_choices])
            pointer_1 = ' ' * (2 * pointing_actions) + '^' if pointing_actions is not None else ''
        elif qia_choices:
            padding_1 = ' ' * (23 - 4 * len(qia_choices))
            action_icons = '  '.join([s[0].__str__()[1:-1] for s in qia_choices])
            pointer_1 = ' ' * (8 * pointing_actions) + '^' if pointing_actions is not None else ''
        else:
            padding_1 = ' ' * 22
            action_icons = '打' if self.__class__.__name__ == 'HmPlayState' else '  '
            pointer_1 = ' ' * (2 * pointing_actions) + '^' if pointing_actions is not None else ''

        pointer_2 = '  ' * (pointing_cards + 3 * len(self.hand_1.private[0])) + '^' if pointing_cards else ''
        padding_2 = ' ' * ((48 - len(self.game_info['hm_name'])) // 2)
        points = sum([s.points for s in self.hand_1.public])
        screen = """
        Game: {round}
        
                             {cpt_name} {cpt_dealer}
        
           [{cpt_private}]
           {cpt_public}
         ______________________________________________
        |                                              |
        |   {table_cpt}
        |                                              |
        |                     [{bench_cpt}]                     |
        |                     [{bench_hm}]                     |
        |                                              |
        |   {table_hm}
        |______________________________________________|
        {padding_1}[{action_icons}]
        {padding_1} {pointer_1}
           {hm_public}
           [{hm_private}]
          {pointer_2}
        {padding_2}{hm_name} {hm_dealer}
        
        ________________________________________________
        your current 胡子:{points}
        bench:{bench_order}
        private_ke:{pk}
        check:{check_fun}
        
        """.format(round=self.game_info['round'],
                   cpt_name=self.game_info['cpt_name'],
                   cpt_dealer=cpt_dealer,
                   cpt_private=cpt_private,
                   cpt_public=cpt_public,
                   table_cpt=table_cpt,
                   bench_cpt=bench_cpt,
                   bench_hm=bench_hm,
                   table_hm=table_hm,
                   padding_1=padding_1,
                   action_icons=action_icons,
                   pointer_1=pointer_1,
                   hm_private=hm_private,
                   hm_public=hm_public,
                   points=points,
                   pointer_2=pointer_2,
                   padding_2=padding_2,
                   hm_name=self.game_info['hm_name'],
                   hm_dealer=hm_dealer,
                   bench_order=self.bench.order if self.bench else '',
                   pk=self.hand_1.orders[0],
                   check_fun=self.hand_1._check_gang_private(self.bench.order) if self.bench else '')
        return screen

    def print_screen(self, pointing_actions=None, action_choices=None, qia_choices=None, pointing_cards=None):
        screen = self.screen(pointing_actions, action_choices, qia_choices, pointing_cards)
        Functions.stdout(screen)
        return

    def pick_cards(self, length):
        pos = 1
        self.print_screen(pointing_cards=pos)
        while True:
            key_in = Functions.stdin()
            if key_in == 'enter' or key_in == 'space':
                return pos
            else:
                if pos > 1 and key_in == 'left':
                    pos -= 1
                elif pos < length and key_in == 'right':
                    pos += 1
            self.print_screen(pointing_cards=pos)

    def pick_actions(self, icons):
        pos = 0
        self.print_screen(pointing_actions=pos, action_choices=icons)
        while True:
            key_in = Functions.stdin()
            # if key_in == 'esc':
            #     import sys
            #     sys.exit()
            if key_in == 'enter' or key_in == 'space':
                return icons[pos]
            else:
                if pos > 0 and key_in == 'left':
                    pos -= 1
                elif pos < len(icons)-1 and key_in == 'right':
                    pos += 1
            self.print_screen(pointing_actions=pos, action_choices=icons)

    def pick_qia(self, qia_choices):
        pos = 0
        self.print_screen(pointing_actions=pos, qia_choices=qia_choices)
        while True:
            key_in = Functions.stdin()
            if key_in == 'enter' or key_in == 'space':
                return qia_choices[pos]
            elif key_in == 'esc':
                return None
            else:
                if pos > 0 and key_in == 'left':
                    pos -= 1
                elif pos < len(qia_choices)-1 and key_in == 'right':
                    pos += 1
            self.print_screen(pointing_actions=pos, qia_choices=qia_choices)

    def check_(self, player_id):
        print("player "+str(player_id)+' is now checking...'+self.bench.hanzi)
        available = getattr(self, 'hand_'+str(player_id)).check(self.bench)
        icons = []
        if 'pao' in available:
            icons.append(5)
        elif 'gang' in available:
            icons.append(4) if self.turn == self.owner else icons.append(5)
        elif 'ke' in available and self.turn == self.owner:
            icons.append(3)
        else:
            if 'ke' in available:
                icons.append(2)
            if 'qia' in available \
                    and self.bench.order not in [x.order for x in self.table[0]] \
                    and self.bench.order not in [x.order for x in self.table[1]]:
                icons.append(1)
                if self.bench.order in getattr(self, 'hand_'+str(player_id)).orders[1]:
                    # check luodiability

                    pass
            if 'guo' in available:
                icons.append(0)
        print(available)
        _ = Functions.stdin()
        return sorted(icons), available


class DealState(Gamestate):

    def __init__(self, game_info):
        self.dealer = game_info['dealer']
        hand_1, hand_2, the_21, pool = DealState.deal(self.dealer)
        super().__init__(game_info, hand_1, hand_2, 0, 0, self.dealer, ([], []), None, pool)
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
        hand_1 = Hand([[], cards_1], [])
        hand_2 = Hand([[], cards_2], [])

        hand_1.init_sort()
        hand_2.init_sort()
        return hand_1, hand_2, the_21, pool

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
        if self.owner == 1:
            return CptStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 1, self.table, self.bench, self.pool)
        else:
            self.table[0].append(self.bench)
            return HmOpenState(self.game_info, self.hand_1, self.hand_2, self.source, self.table, self.pool)

    def next_(self):
        icons, available = self.check_(1)
        # actions = [0, 2, 5], available = {'guo': [], 'beng': [], 'gang': ['private', idx]}
        while True:
            pick = self.pick_actions(icons)
            if pick == 0:
                return self.pass_()
            elif pick == 4 or pick == 5:
                # dia or pao
                getattr(self.hand_1, ACTIONS[pick])(self.bench, available['gang'][0], available['gang'][1])
                if len([gang for gang in self.hand_1.public if gang.__class__.__bases__[0].__name__ == 'Gang']) > 1:
                    return CptOpenState(self.game_info, self.hand_1, self.hand_2, self.source, self.table, self.pool)
                else:
                    return HmPlayState(self.game_info, self.hand_1, self.hand_2,
                                       self.source, self.owner, self.table, self.pool)
            elif pick == 2 or pick == 3:
                # beng or xiao
                getattr(self.hand_1, ACTIONS[pick])(self.bench)
                return HmPlayState(self.game_info, self.hand_1, self.hand_2,
                                   self.source, self.owner, self.table, self.pool)
            elif pick == 1:
                # qia
                qia_method = self.pick_qia(available['qia'])
                if not qia_method:
                    continue
                self.hand_1.qia(qia_method)
                return HmPlayState(self.game_info, self.hand_1, self.hand_2,
                                   self.source, self.owner, self.table, self.pool)


class HmOpenState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, 2, 1, table, None, pool)

    def open_(self):
        new_card = self.pool.deal()
        self.bench = new_card
        icons, _ = self.check_(2)
        if 5 in icons or 2 in icons:
            return CptStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 1, self.table, new_card, self.pool)
        else:
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
        pick_pos = self.pick_cards(len(self.hand_1.private[1]))
        played_card = self.hand_1.play(pick_pos-1)
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
        icons, available = self.check_(2)
        # actions = [0, 2, 5], available = {'guo': [], 'beng': [], 'gang': ['private', idx]}
        pick = 0 if max(icons) < 2 else icons[-1]
        # pick = 4 (if click 5)
        if pick == 0:
            return self.pass_()
        elif pick == 4 or pick == 5:
            # dia or pao
            getattr(self.hand_2, ACTIONS[pick])(self.bench, available['gang'][0], available['gang'][1])
            if len([gang for gang in self.hand_2.public if gang.__class__.__bases__[0].__name__ == 'Gang']) > 1:
                return HmOpenState(self.game_info, self.hand_1, self.hand_2, self.source, self.table, self.pool)
            else:
                return CptPlayState(self.game_info, self.hand_1, self.hand_2,
                                    self.source, self.owner, self.table, self.pool)
        elif pick == 2 or 3:
            # beng or xiao
            getattr(self.hand_2, ACTIONS[pick])(self.bench)
            return CptPlayState(self.game_info, self.hand_1, self.hand_2,
                                self.source, self.owner, self.table, self.pool)


class CptOpenState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, table, pool):
        super().__init__(game_info, hand_1, hand_2, source, 1, 2, table, None, pool)

    def open_(self):
        new_card = self.pool.deal()
        self.bench = new_card
        icons, _ = self.check_(1)
        if 5 in icons or 2 in icons:
            return HmStrategyState(self.game_info, self.hand_1, self.hand_2, 2, 2, self.table, new_card, self.pool)
        else:
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
        played_card = self.hand_2.rand_play()
        return HmStrategyState(self.game_info, self.hand_1, self.hand_2, 1, 2, self.table, played_card, self.pool)

    def next_(self):
        return self.auto_play()


class DrawGameState(Gamestate):

    def __init__(self, game_info, hand_1, hand_2, source, owner, turn, table, bench, pool):
        super().__init__(game_info, hand_1, hand_2, source, owner, turn, table, bench, pool)
        self.end = True
