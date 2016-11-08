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

    def absorb(self, ruler, chosen_color):
        ruler_array_copy = [[0 for x in range(self.width)] for y in range(self.height)]

        for y in range(self.height):  # Fill ruled area with chosen_color.
            for x in range(self.width):
                if self.ruler_array[y][x] == ruler:
                    self.color_array[y][x] = chosen_color

        absorb_repeat = True
        while absorb_repeat:  # Absorb repeatedly for complete absorbing.
            for y in range(self.height):  # Copy ruler_array for repetitive absorbing.
                for x in range(self.width):
                    ruler_array_copy[y][x] = self.ruler_array[y][x]

            for y in range(self.height):  # Absorb.
                for x in range(self.width):
                    if self.ruler_array[y][x] == 0 and self.color_array[y][x] == chosen_color and (
                        # If the area isn't ruled and is filled with chosen color,
                        (x > 0 and self.ruler_array[y][x - 1] == ruler)  # Check left side,
                        or (x < (self.width - 1) and self.ruler_array[y][x + 1] == ruler)  # Check right side,
                        or (y > 0 and self.ruler_array[y - 1][x] == ruler)  # Check up side,
                        or (y < (self.height - 1) and self.ruler_array[y + 1][x] == ruler)  # Check down side,
                    ):  # If ruler's area is adjacent,
                        self.ruler_array[y][x] = ruler  # Rule the area.

            absorb_repeat = False
            check_stop = False
            # If ruler_array == ruler_array_copy, finish absorbing.
            # = If there isn't any change after absorbing, absorbing is complete, so finish absorbing.
            for y in range(self.height):
                if check_stop:
                    break
                for x in range(self.width):
                    if self.ruler_array[y][x] != ruler_array_copy[y][x]:
                        absorb_repeat = True
                        check_stop = True  # To escape from outer for loop.
                        break