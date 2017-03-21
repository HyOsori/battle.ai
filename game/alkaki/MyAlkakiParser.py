from game.alkaki.AlkakiParser import ALKAKIParser

import game.debugger as logging


class MyALKAKIParser(ALKAKIParser):
    def __init__(self):
        pass

    def game_phase(self):
        raise NotImplementedError
