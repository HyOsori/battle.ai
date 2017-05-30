from game.alkaki.alkaki_parser import ALKAKIParser


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
    def get_predict_position(self, x_pos, y_pos, x_dir, y_dir, speed):
        while speed > 0:
            x_pos += x_dir * speed
            y_pos += y_dir * speed
            speed -= 0.1

        if x_pos < 0 or x_pos > 100 or y_pos < 0 or y_pos > 100:
            return "out"

        return {
            "x": x_pos,
            "y": y_pos,
        }
