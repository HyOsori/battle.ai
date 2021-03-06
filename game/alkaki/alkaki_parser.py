# -*-coding:utf-8-*-
import sys

from gamebase.client.AIParser import AIParser

import utils.debugger as logging

sys.path.insert(0, '../')


class ALKAKIParser(AIParser):
    def __init__(self):
        pass

    def init_phase(self, init_data):
        pass

    def parsing_data(self, decoding_data):
        base = super(ALKAKIParser, self).parsing_data(decoding_data)
        logging.info("PARSING DATA")

        return_dict = self.game_phase(decoding_data)
        return self.make_send_msg('game', return_dict)

    def game_phase(self, board_data):
        raise NotImplementedError
