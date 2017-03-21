from game.alkaki.AlkakiParser import ALKAKIParser

import game.debugger as logging


class MyALKAKIParser(ALKAKIParser):
    def __init__(self):
        pass

    def init_phase(self, init_data):
        test = 'test'

    def game_phase(self):
        return {'data': 'parser_test'}
