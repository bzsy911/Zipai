# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 11:06:00 2018

@author: PG738LD
"""

from collections import Counter, deque
import sys, os

HANZI = {
    1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十',
    101: '壹', 102: '贰', 103: '叁', 104: '肆', 105: '伍', 106: '陆', 107: '柒', 108: '捌', 109: '玖', 110: '拾',
    'guo': '过', 'qia': '吃', 'beng': '碰', 'xiao': '笑', 'dia': '掉', 'pao': '跑', 'fu': '胡'}

ACTIONS = {0: 'guo', 1: 'qia', 2: 'beng', 3: 'xiao', 4: 'dia', 5: 'pao', 6: 'fu'}

patterns = ["shun", "2710", "mixed", "liangjia", "pa270", "pashun", "pamixed"]

WIN_KEYMAP = {27: 'esc', 110: 'n', 72: 'up', 80: 'down', 77: 'right', 75: 'left', 13: 'enter', 32: 'space'}
MAC_KEYMAP = {27: 'esc', 110: 'n', 65: 'up', 66: 'down', 67: 'right', 68: 'left', 10: 'enter', 32: 'space'}


class SCREEN:
    welcome = """
    * * * * * * * * * * * * * * * * * *
    *                                 *
    *    Welcome to Hengyang Zipai    *
    *                                 *
    *           version 0.4           *
    *                                 *
    * * * * * * * * * * * * * * * * * *
    
        Press any key to start Game
    
    
    ===================================
    Quit(ESC)
    Copyright \xa9 2018 Stella & Co.
    
    """
    
    farewell = """
    * * * * * * * * * * * * * * * * * *
    *                                 *
    *            Good Bye.            *
    *                                 *
    *  Hengyang Zipai, a Stella game. *
    *                                 *
    * * * * * * * * * * * * * * * * * *
    
        Directed by    STELLA CHEN
        Produced by    HONGFEI TIAN
    
    ===================================
    Contact: jchen417@gmail.com
             bzsy911@gmail.com
    """


class Analyzer:
    """All card related calculation functions.
    Will move lots of Hand methods here."""

    @staticmethod
    def check_fu(ls):
        res = []
        queue = deque([([], ls)])
        while queue:
            sets, cards = queue.popleft()
            if not cards:
                sets.sort()
                if sets not in res:
                    res.append(sets)
            elif len(cards) == 2:
                if cards[0] == cards[1]:
                    sets.append(['Pair', cards[0], cards])
                    sets.sort()
                    if sets not in res:
                        res.append(sets)
            elif len(cards) >= 3:
                for s in Analyzer._find_all(cards):
                    queue.append((sets + [s], Functions.take_out(cards, s[2])))
        return res

    @staticmethod
    def _find_all(ls):
        return Analyzer._find_ke(ls) + Analyzer._find_shun(ls) + Analyzer._find_mixed(ls)

    @staticmethod
    def _find_ke(ls):
        return [['Ke', x, [x, x, x]] for x in set(ls) if ls.count(x) == 3]

    @staticmethod
    def _find_shun(ls):
        res = []
        d = sorted(list(set(ls)))
        if len(d) < 3:
            return []
        for i in range(len(d) - 2):
            if d[i + 1] == d[i] + 1 and d[i + 2] == d[i] + 2:
                if d[i] % 100 == 1:
                    res.append(['YiErSan', d[i]//100, d[i:i+3]])
                else:
                    res.append(['Shun', d[i+1], d[i:i + 3]])
        if {102, 107, 110} <= set(ls):
            res.append(['ErQiShi', 1, [102, 107, 110]])
        if {2, 7, 10} <= set(ls):
            res.append(['ErQiShi', 0, [2, 7, 10]])
        return res

    @staticmethod
    def _find_mixed(ls):
        res = []
        d = sorted(ls, key=lambda x: x % 100)
        if len(d) < 3:
            return []
        for i in range(len(d)-2):
            if len(set([x % 100 for x in d[i:i+3]])) == 1 and 100 < sum(d[i:i+3]) < 300:
                res.append(['Mixed', [d[i] % 100, sum(d[i:i+3]) > 200], sorted(d[i:i+3])])
        return res


class Functions:

    @staticmethod
    def take_out(ls, pattern):
        return list((Counter(ls)-Counter(pattern)).elements())

    @staticmethod
    def has_n(ls, n):
        for (ele, cnt) in Counter(ls).items():
            if cnt == n:
                return ele
        return None

    @staticmethod
    def stdout(screen):
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        print(screen)

    @staticmethod
    def stdin():
        in_key = _Getch()
        key = ord(in_key())
        if sys.platform == 'win32':
            try:
                return WIN_KEYMAP[key]
            except KeyError:
                return 'any'
        if sys.platform == 'darwin':
            try:
                return MAC_KEYMAP[key]
            except KeyError:
                return 'any'
        else:
            # Linux case to be implemented
            return 'any'


class _Getch:

    def __init__(self):
        if sys.platform == 'win32':
            import msvcrt
            self.impl = msvcrt.getch()
        elif sys.platform == 'darwin':
            import getch
            self.impl = getch.getch()
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            self.impl = ch

    def __call__(self): 
        return self.impl


if __name__ == '__main__':
    from objects import Pool
    while True:
        # p = Pool()
        # cards, a = p.deal_hand(1)[0], p.deal()
        # hand = sorted([x.order for x in cards + [a]])
        # print(hand)
        hand = [1,2,2,3,5,5,5,7,10]
        check = Analyzer.check_fu(hand)
        print(check)
        key_in = Functions.stdin()
        if key_in == 'enter' or key_in == 'space':
            break
