# -*-coding:utf-8-*-
from gameLogic.pixels.PixelsParser import PixelsParser
import random


class MyPixelsParser(PixelsParser):
    def loop_phase(self):

        width = self.game_data['width']
        height = self.game_data['height']
        color_array = self.game_data['color_array']
        ruler_array = self.game_data['ruler_array']
        start_point_y = self.game_data['start_point_y']
        start_point_x = self.game_data['start_point_x']
        ruler_self = self.game_data['ruler_self']
        ruler_enemy = self.game_data['ruler_enemy']
        enemy_chosen_color = self.game_data['enemy_chosen_color']

        if ruler_self == 1:
            my_color = color_array[start_point_x[0]][start_point_y[0]]
        elif ruler_self == 2:
            my_color = color_array[start_point_x[1]][start_point_y[1]]

        return_color = random.randint(1, 6)
        while return_color == enemy_chosen_color or return_color == my_color:
            return_color = random.randint(1, 6)

        parsing_data = {'chosen_color': return_color}

        send_msg = self.make_send_msg(self.msg_type, parsing_data)
        return send_msg
