#-*-coding:utf-8-*-
import base64
import json
import sys
import zlib

sys.path.insert(0,'../')
from gamebase.client.AIParser import AIParser

class PixelsParser(AIParser):
    def __init__(self):
        pass

    def parsing_data(self, decoding_data):
        base = super(PixelsParser, self).parsing_data(decoding_data)
        ret = None
        if self.msg_type == 'loop':
            if self.game_data['enemy_chosen_color'] != None:
                self.absorb(self.game_data['ruler_enemy'], self.game_data['enemy_chosen_color'])
            ret = self.loop_phase()
            self.absorb(self.game_data['ruler_self'], ret['chosen_color'])
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
        print('notify_loop_init get!')
        self.width = self.game_data['width']
        self.height = self.game_data['height']
        self.color_array = json.loads(zlib.decompress(base64.b64decode(self.game_data['color_array'])))
        self.ruler_array = [[0 for x in range(self.width)] for y in range(self.height)]

        ys = self.game_data['start_point_y']
        xs = self.game_data['start_point_x']
        self.ruler_array[ys[0]][xs[0]] = 1
        self.ruler_array[ys[1]][xs[1]] = 2

        self.color_array_old = self.copy_array(self.color_array)
        self.ruler_array_old = self.copy_array(self.ruler_array)
        return None

    def notify_change_round(self):
        print('notify_change_round get!')
        self.color_array = self.copy_array(self.color_array_old)
        self.ruler_array = self.copy_array(self.ruler_array_old)

        ys = self.game_data['start_point_y']
        xs = self.game_data['start_point_x']
        self.ruler_array[ys[0]][xs[0]] = 1
        self.ruler_array[ys[1]][xs[1]] = 2
        return None

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

    def copy_array(self, array):
        retrun_array = [[array[y][x] for x in range(self.width)] for y in range(self.height)]
        return retrun_array

    def print_array(self, array):
        '''
        for debug
        :param array:
        :return:
        '''
        print('array print: ')
        for y in range(self.height):
            for x in range(self.width):
                sys.stdout.write(str(array[y][x])+' ')
            print('')

    def ruler_setting(self, start_point_y, start_point_x):
        pass