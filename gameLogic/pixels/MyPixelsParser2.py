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

        '''
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (RulerArray[y][x] == 0 and (
                        # If the area isn't ruled
                                    (x > 0 and RulerArray[y][x - 1] == ruler) or  # Check left side
                                    (x < (WIDTH - 1) and RulerArray[y][x + 1] == ruler) or  # Check right side
                                (y > 0 and RulerArray[y - 1][x] == ruler) or  # Check up side
                            (y < (HEIGHT - 1) and RulerArray[y + 1][x] == ruler))):  # Check down side
                    NumOfEachColor[colornumarray[y][x]] = NumOfEachColor[
                                                              colornumarray[y][x]] + 1  # We can rule the area

        max = 0
        returncolornum = random.randint(1, 6)
        while (returncolornum == exclusionnum or returncolornum == mycolornum):
            returncolornum = random.randint(1, 6)
        NumOfEachColor[0] = -1

        for i in range(NumOfColor + 1):
            if (NumOfEachColor[i] > max and i != mycolornum and i != exclusionnum):
                max = NumOfEachColor[i]
                returncolornum = i

        return returncolornum
        '''

        return_color = random.randint(1, 6)
        while return_color == enemy_chosen_color or return_color == my_color:
            return_color = random.randint(1, 6)

        parsing_data = {'chosen_color': return_color}

        send_msg = self.make_send_msg(self.msg_type, parsing_data)
        return send_msg
