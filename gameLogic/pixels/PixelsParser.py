#-*-coding:utf-8-*-
import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.AIParser import AIParser

class PixelsParser(AIParser):
    def __init__(self):
        pass

    def parsing_data(self, decoding_data):
        base = super(PixelsParser, self).parsing_data(decoding_data)
        if self.msg_type == 'loop':
            return self.loop_phase()
        return base

    def loop_phase(self):
        '''
        must override
        :return:
        '''
        pass