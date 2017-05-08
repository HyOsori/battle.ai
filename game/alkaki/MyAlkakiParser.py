from game.alkaki.AlkakiParser import ALKAKIParser

import game.debugger as logging
import random

class MyALKAKIParser(ALKAKIParser):
    def __init__(self):
        self.board_size = None
        self.count = None
        self.radius = None
        self.player_pos = None

    def init_phase(self, init_data):
        self.board_size = init_data['board_size']
        self.count = init_data['count']
        self.radius = init_data['radius']
        self.player_pos = init_data['player_pos']

    def game_phase(self, board_data):

        index = 0
        direction = [1, 0]
        force = 3

        return_dict = {
            'index': index,
            'direction': direction,
            'force': force
        }

        return return_dict
