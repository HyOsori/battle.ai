# -*-coding:utf-8-*-
import sys
from gamebase.client.AIParser import AIParser
import game.debugger as logging

sys.path.insert(0, '../')


class ALKAKIParser(AIParser):
    def __init__(self):
        pass

    def init_phase(self, init_data):
        pass

    def parsing_data(self, decoding_data):
        base = super(ALKAKIParser, self).parsing_data(decoding_data)
        logging.info("PARSING DATA")

        ret = None
        ret = self.game_phase()
        return self.make_send_msg('game', ret)

    def game_phase(self):
        raise NotImplementedError
