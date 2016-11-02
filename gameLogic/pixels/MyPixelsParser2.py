# -*-coding:utf-8-*-
from gameLogic.pixels.PixelsParser import PixelsParser
import random


class MyPixelsParser2(PixelsParser):
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

        num_of_color = 6
        num_of_each_color = [0 for i in range(num_of_color + 1)]

        if ruler_self == 1:
            my_color = color_array[start_point_x[0]][start_point_y[0]]
        elif ruler_self == 2:
            my_color = color_array[start_point_x[1]][start_point_y[1]]

        for y in range(height):
            for x in range(width):
                if (ruler_array[y][x] == 0) and (
                    (x > 0 and ruler_array[y][x - 1] == ruler_self)  # Check left side
                    or (x < (width - 1) and ruler_array[y][x + 1] == ruler_self)  # Check right side
                    or (y > 0 and ruler_array[y - 1][x] == ruler_self)  # Check up side
                    or (y < (height - 1) and ruler_array[y + 1][x] == ruler_self)  # Check down side
                ):  # Count the number of area that we can rule, with dividing according to colors.
                    num_of_each_color[color_array[y][x]] += 1

        max_num = 0

        return_color = random.randint(1, 6)
        while return_color == enemy_chosen_color or return_color == my_color:
            return_color = random.randint(1, 6)

        num_of_each_color[0] = -1
        for i in range(num_of_color + 1):
            if num_of_each_color[i] > max_num and i != my_color and i != enemy_chosen_color:
                max_num = num_of_each_color[i]
                return_color = i

        parsing_data = {'chosen_color': return_color}

        send_msg = self.make_send_msg(self.msg_type, parsing_data)
        return send_msg
