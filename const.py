# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 11:06:00 2018

@author: PG738LD
"""

from collections import Counter 
import sys, os

HANZI = {
         1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 
         8: '八', 9: '九', 10: '十', 101: '壹', 102: '贰', 103: '叁', 
         104: '肆', 105: '伍', 106: '陆', 107: '柒', 108: '捌', 109: '玖',
         110: '拾'   
        }

patterns = ["shun", "2710", "mixed", "liangjia", "pa270", "pashun", "pamixed"]

WIN_KEYMAP = {27: 'esc', 110: 'n', 72: 'up', 80: 'down', 77: 'right', 75: 'left', 13: 'enter', 32: 'space'}
MAC_KEYMAP = {27: 'esc', 110: 'n', 65: 'up', 66: 'down', 67: 'right', 68: 'left', 10: 'enter', 32: 'space'}


class SCREEN:
    welcome = """
    * * * * * * * * * * * * * * * * * *
    *                                 *
    *    Welcome to Hengyang Zipai    *
    *                                 *
    *           version 0.3           *
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
    

class Functions:

    @staticmethod
    def explode(node):
        res = []
        for pattern in patterns:
            pass
        pass

    @staticmethod
    def take_out(ls, pattern):
        return list((Counter(ls)-Counter(pattern)).elements())

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
    while True:
        key_in = Functions.stdin()
        print(key_in)
        if key_in == 'enter' or key_in == 'space':
            break
