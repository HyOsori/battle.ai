#-*-coding:utf-8-*-
import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.AIParser import AIParser

class PixelsParser(AIParser):
    def __init__(self):
        pass

    def parsing_data(self, decoding_data):
        base = super(PixelsParser, self).parsing_data(decoding_data)
        ret = None
        if self.msg_type == 'loop':
            ret = self.loop_phase()
        if ret == None:
            return base
        else:
            return self.make_send_msg(self.msg_type,ret)

    def loop_phase(self):
        '''
        must override
        :return:
        '''
        pass