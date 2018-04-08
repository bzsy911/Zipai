# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 11:06:00 2018

@author: PG738LD
"""

from collections import Counter 

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
    *           version 0.1           *
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

    def explode(node):
        res = []
        for pattern in patterns:
            pass
        pass
            
    
    
    def take_out(ls, pattern):
        return list((Counter(ls)-Counter(pattern)).elements())
        

class _Getch:

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMac()
            except AttributeError:
                self.impl = _GetchUnix()

    def __call__(self): 
        return self.impl()


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class _GetchUnix:
    def __init__(self):
        import tty, sys, termios 
        
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchMac:
    def __init__(self):
        import getch

    def __call__(self):
        import getch
        return getch.getch()




if __name__ == '__main__':
    print('Press a key')
    inkey = _Getch()
    while True:
        k = inkey()
        print(ord(k))
        if ord(k) == 27:
            break
        print('you pressed ', str(k))
    print('you pressed', k)