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


class SCREEN:
    welcome = """
    * * * * * * * * * * * * * * * * * *
    *                                 *
    *    Welcome to Hengyang Zipai    *
    *                                 *
    *           version 0.2           *
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
        return ord(in_key())
        

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
