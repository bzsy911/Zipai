# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 13:40:04 2018

@author: PG738LD
"""

import sys
from const import Functions, SCREEN
from game import Game


class Zipai:
    """
    version 0.2
    """
    Version = 0.2
    
    def __init__(self):
        self.games = []
        Zipai.welcome()
        Functions.stdout('')
        prompt_name = '\n'*3 + ' '*10 + 'What\'s you name?\n' + ' '*13
        hm_name = input(prompt_name)
        self.user_info = {'hm_name': hm_name,
                          'cpt_name': 'Stella'}

    def start(self):
        in_key = ''
        while in_key != 'n':
            self.user_info['round'] = len(self.games) + 1
            game = self.new_game(len(self.games) % 2+1)
            for _ in game:
                pass

            print("No more card. Draw Game!")
            print("Start a new game? (any/n)")
            in_key = Functions.stdin()
        Zipai.end()

    @staticmethod
    def welcome():
        """Welcome Page
        Press any key to start the first game.
        Press ESC to quit."""
        Functions.stdout(SCREEN.welcome)
        in_key = Functions.stdin()
        if in_key == 'esc':
            Zipai.end()
        return
    
    @staticmethod
    def end():
        """Farewell Page"""
        Functions.stdout(SCREEN.farewell)
        sys.exit()
    
    def new_game(self, n):
        """Start a new game.
        n: int, id of dealer, who won the last game."""
        game = Game(n, self.user_info)
        self.games.append(game)
        return game


if __name__ == '__main__':
    a = Zipai()
    a.start()