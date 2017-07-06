from game.alkaki.alkaki_parser import ALKAKIParser
import math


class MyALKAKIParser(ALKAKIParser):
    def __init__(self):
        self.board_size = None
        self.count = None
        self.radius = None
        self.player_pos = None

    def init_phase(self, init_data):
        self.board_size = init_data['board_size']
        self.count = init_data['count']
        self.radius = init_data['radius']
        self.player_pos = init_data['player_pos']

    def game_phase(self, board_data):

        index = 0
        direction = [1, 0]
        force = 3

        return_dict = {
            'index': index,
            'direction': direction,
            'force': force
        }
        return return_dict

    # Logic Side
    @staticmethod
    def get_direction_depending_on_position(x_prev, y_prev, x_next, y_next):
        pass

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

