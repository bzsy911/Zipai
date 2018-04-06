# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 13:40:04 2018

@author: PG738LD
"""


import sys, operator, os
import random
from const import _Getch, SCREEN
from objects import Pool
from game import Game

class Zipai:
    """
    version 0.1
    """
    Version = 0.1
    
    def __init__(self):
        self.games = []
    
    def start(self):
        Zipai._stdout(SCREEN.welcome)
        inkey = Zipai._input()
        if inkey == 27:
            self.end()
        inkey == -1
        while inkey != ord('n'):
            self.new_game()
            print("\n\nthis hand seem's not very lovely.")
            print("Do you want to new game? (any/n)")
            
            inkey = Zipai._input()
        self.end()

    
    def end(self):
        Zipai._stdout(SCREEN.farewell)
        sys.exit()
    
    def new_game(self):
        game = Game(0)
        self.games.append(game)
        Zipai._stdout(game.screen())
        return game

    @staticmethod
    def _stdout(screen):
        os.system('cls')
        print(screen)
    
    @staticmethod
    def _input():
        inkey = _Getch()
        return ord(inkey())     



if __name__ == '__main__':
    a = Zipai()
    a.start()







"""


class Game:
    # current version is designed only for 1 human vs 1 AI. 
    # Human play as the Zhuang for the first game.
    def __init__(self, players=2, human=1):
        self.players = players
        self.human = human
        self.round = 0
        self.last_winner = 1
        self.account = 0
        self.state = self.start()
        
    players = property(operator.attrgetter("_players"))
    @players.setter
    def players(self, p):
        if p not in [2,3]:
            raise Exception("This game can only be played by 2 or 3 players.")
        self._players = p
    
    human = property(operator.attrgetter("_human"))
    @human.setter
    def human(self, h):
        if h not in range(1, self._players+1):
            raise Exception("invalid number of human players.")
        self._human = h
    
    def play(self):
        if self.round > 0:
            new = input("new game? (y/n)")
            if new == 'y':
                self.start()
            else:
                print('goodbye!')
                return
        else:
            self.start()
        
    def start(self):
        self.round += 1
        game = SingleGame(self.last_winner)
        winner, point = game.run()
        self.last_winner = winner
        self.account += point
        self.play()
        
            
        
class SingleGame:
    def __init__(self, zhuang):
        # zhuang = 0 for AI, 1 for human.
        self.zhuang = zhuang
        self.state = self.distribute()
        
    def distribute(self):
        deck = SingleGame.shuffle()
        zhuang = Hand(sorted(deck[:21]), [])
        xian = Hand(sorted(deck[21:41]), [])
        if self.zhuang:
            state = State(xian, zhuang, [], deck[41:])
        else:
            state = State(zhuang, xian, [], deck[41:])
        return state
    
    @staticmethod
    def shuffle():
        genesis = []
        for i in range(10):
            genesis.extend([i+1, i+101] * 4)
        random.shuffle(genesis)
        return genesis

    def run(self):
        while not self.state.is_win[0]:
            self.print_state()
            self.state = self.state.run()
        print("winner is player" + str(self.state.is_win[1]))
        return self.state.is_win[1:]
    
    def print_state(self):
        print(['X' * len(self.state.p0.hand)])
        print(self.state.p0.desk)
        print('*' * 20)
        print()
        print(self.state.table)
        print('card left: '+str(len(self.state.pool)))
        print()
        print('*' * 20)
        print(self.state.p1.desk)
        print(self.state.p1.hand)
            
        

class Hand:    
    def __init__(self, hand, desk):
        self.hand = hand
        self.desk = desk
        

class State:
    
    def __init__(self, p0, p1, table, pool):
        self.p0 = p0
        self.p1 = p1
        self.table = table
        self.pool = pool
        self.is_win = [False, -1, 0]
        self.action = 0 if len(self.p0.hand) == 21 else 1
    
    def run(self):
        
        self.is_win = [True, 1, 1]
        return self
        
"""
