from battle_player.base.LogicHandler import LogicHandler
from utils.constant import *
import math


class CustomAlkakiLogic(LogicHandler):

    def __init__(self):
        """
        Develop own your OMOK AI
        width and height are board's width and height
        empty place is represented integer 0
        and your color is represented by number 0 1 2 ...

        your color is set automatically.
        """
        self.board_size = None
        self.count = None
        self.radius = None
        self.player_pos = None

    def init_phase(self, msg_type, data):
        """
        :param msg_type:
        :param data:
        :param init_data: {"width": (Integer), "height": (Integer), "color": (Integer)}
        :return: None
        """
        self.board_size = data['board_size']
        self.count = data['count']
        self.radius = data['radius']
        self.player_pos = data['player_pos']
        return msg_type, {"response": "OK"}

    def loop_phase(self, msg_type, data):
        index = 0
        my_arr = data['my_arr']
        enemy_arr = data['enemy_arr']

        direction = self.get_direction_depending_on_position(0, 0, 3, 3)
        force = self.get_distance(my_arr[0][0], my_arr[0][1], enemy_arr[0][0], enemy_arr[0][1])

        if force > 5:
            force = 5

        return_dict = {
            'index': index,
            'direction': direction,
            'force': force
        }
        return msg_type, return_dict

    # Logic Side
    def get_direction_depending_on_position(self, x_prev, y_prev, x_next, y_next):
        x_dir = (x_next - x_prev) / self.get_distance(x_prev, y_prev, x_next, y_next)
        y_dir = (y_next - y_prev) / self.get_distance(x_prev, y_prev, x_next, y_next)
        return [x_dir, y_dir]

    @staticmethod
    def get_force_depending_on_distance(distance):
        force = 0
        force_increase = 0.1
        while force < distance:
            force = force + force_increase
            force_increase = force_increase + 0.1

        return force

    @staticmethod
    def get_distance(x_prev, y_prev, x_next, y_next):
        return math.sqrt(
            math.pow(x_next - x_prev, 2) +
            math.pow(y_next - y_prev, 2))