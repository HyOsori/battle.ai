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
        if self.msg_type == 'notify_init_loop':
            ret = self.notify_loop_init()
        if self.msg_type == 'notify_change_round':
            ret = self.notify_change_round()
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

    def notify_loop_init(self):
        print 'notify_loop_init get!'
        self.color_array = self.game_data['color_array']
        self.ruler_array = self.game_data['ruler_array']
        self.width = self.game_data['width']
        self.height = self.game_data['height']

        self.color_array_old = self.game_data['color_array']
        self.ruler_array_old = self.game_data['ruler_array']
        return None

    def notify_change_round(self):
        print 'notify_change_round get!'
        self.color_array = self.color_array_old
        self.ruler_array = self.ruler_array_old
        print self.color_array, self.ruler_array
        return None