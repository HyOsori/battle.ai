# -*-coding:utf-8-*-
import random

from game.pixels.PixelsParser import PixelsParser


class MyPixelsParser2(PixelsParser):
    def loop_phase(self):
        width = self.width
        height = self.height
        color_array = self.color_array
        ruler_array = self.ruler_array
        start_point_y = self.game_data['start_point_y']
        start_point_x = self.game_data['start_point_x']
        ruler_self = self.game_data['ruler_self']
        ruler_enemy = self.game_data['ruler_enemy']
        enemy_chosen_color = self.game_data['enemy_chosen_color']

        mycolor = self.color_array[start_point_y[ruler_self - 1]][start_point_x[ruler_self - 1]]

        print("before select color")
        print("mycolor" + str(mycolor) + "  eneny_chonsen_color" + str(enemy_chosen_color))
        color = random.randint(1, 6)
        if enemy_chosen_color:
            while color == mycolor or color == enemy_chosen_color:
                color = random.randint(1, 6)
                print("color loop: " + str(color) + "   mycolor" + str(mycolor) + "  eneny_chonsen_color" + str(enemy_chosen_color))
        print("after select color")

        return_color = color

        output_data = {'chosen_color': return_color}
        return output_data
