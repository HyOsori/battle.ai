import sys
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic
from gameLogic.baseClass.Phase import Phase
import logging
import random

sys.path.insert(0, '../')
logging.basicConfig(level=logging.DEBUG)

'''
ShardDict Key

PHASE_LOOP -> 'loop'->
PHASE_FINISH -> 'finish'->

At PixelsGameLogic
width : The width of board
height : The height of board
color_array_init : initialized color_array
start_point_y : [start_point_y of ruler1, start_point_y of ruler2]
start_point_x : [start_point_x of ruler1, start_point_x of ruler2]

At PixelsLoopPhase
score : [1st round[ruler1, ruler2], 2nd round[ruler1, ruler2]]
'''


class PixelsLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsLoopPhase, self).__init__(logic_server, message_type)
        logging.debug('PHASE_LOOP : INIT')

        # Pycharm recommends us not to define instance attribute outside __init__.

        # Initialize variables from outside.
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()
        self.next_phase = self.shared_dict['PHASE_FINISH']
        self.width = self.shared_dict['width']
        self.height = self.shared_dict['height']
        self.start_point_y = self.shared_dict['start_point_y']
        self.start_point_x = self.shared_dict['start_point_x']

        # Initialize variables.
        self.round = 0  # Check Rounds.
        self.initialize = False  # Initialize arrays if new round starts.
        self.score = [[0, 0], [0, 0]]  # Record the scores of two rounds.
        self.chosen_color = 0

        # Declare arrays.
        # Use these arrays in the form of 'array[y][x]'.
        self.color_array = [[0 in range(self.width)] in range(self.height)]
        self.color_array_old = [[0 in range(self.width)] in range(self.height)]
        # Copy color_array to notify front_end of the before/after change in color_array.
        self.ruler_array = [[0 in range(self.width)] in range(self.height)]
        self.ruler_array_copy = [[0 in range(self.width)] in range(self.height)]
        # Copy ruler_array for complete absorbing at absorb().

    def on_start(self):
        super(PixelsLoopPhase, self).on_start()
        logging.debug('PHASE_LOOP : START')

        # Initialize the arrays.
        self.initialize_arrays()
        # self.start_point = [3 / 8, 5 / 8]
        # ruler1 starts at 3/8 point of board.
        self.ruler_array[self.start_point_y[0]][self.start_point_x[0]] = 1
        # ruler2 starts at 5/8 point of board.
        self.ruler_array[self.start_point_y[1]][self.start_point_x[1]] = 2

    def do_action(self, pid, dict_data):
        super(PixelsLoopPhase, self).do_action(pid, dict_data)
        logging.debug('PHASE_LOOP : DO_ACTION / pid : ' + pid)

        if self.initialize:  # Initialize the arrays if new(2nd) round starts.
            self.initialize_arrays()
            # self.start_point = [3 / 8, 5 / 8]
            self.switch_start_point()
            # self.start_point = [5 / 8, 3 / 8]

            # ruler2 starts at 5/8 point of board.
            self.ruler_array[self.start_point_y[0]][self.start_point_x[0]] = 1
            # ruler1 starts at 3/8 point of board.
            self.ruler_array[self.start_point_y[1]][self.start_point_x[1]] = 2

            self.initialize = False

        if self.round == 2:  # Change phase if two rounds are finished.
            self.shared_dict['score'] = self.score
            logging.debug('LoopPhase -> FinishPhase')
            self.change_phase(self.next_phase)

        ruler = 0
        if pid == self.player_list[0]:
            ruler = 1
        if pid == self.player_list[1]:
            ruler = 2
        self.chosen_color = dict_data['chosen_color']

        # Copy color_array to notify front_end of the before/after change in color_array.
        for y in range(self.height):
            for x in range(self.width):
                self.color_array_old[y][x] = self.color_array[y][x]

        self.absorb(ruler, self.chosen_color)

        if self.check_status():  # If check_status returns True, the round is finished.
            self.round += 1
            self.initialize = True

        ruler_enemy = ruler  # Ruler who finished absorbing
        ruler_self = ruler % 2 + 1  # Ruler who will take the request
        self.request_to_client(ruler_self, ruler_enemy)
        self.notify_to_front(ruler)

    def on_end(self):
        super(PixelsLoopPhase, self).on_end()
        logging.debug('PixelsLoopPhase.on_end')

    def switch_start_point(self):
        temp_y = self.start_point_y[0]
        self.start_point_y[0] = self.start_point_y[1]
        self.start_point_y[1] = temp_y
        temp_x = self.start_point_x[0]
        self.start_point_x[0] = self.start_point_x[1]
        self.start_point_x[1] = temp_x

    def notify_to_front(self, ruler):
        notify_dict = {
            'width': self.width,
            'height': self.height,
            'color_array_old': self.color_array_old,
            'color_array': self.color_array,
            'ruler_array': self.ruler_array,
            'ruler_who': ruler,  # Who just finished absorbing
            'score': self.score
        }
        self.notify(notify_dict)

    def request_to_client(self, ruler_self, ruler_enemy):
        logging.debug('Request ' + self.now_turn() + '\'s decision')
        info_dict = {
            'width': self.width,
            'height': self.height,
            'color_array': self.color_array,
            'ruler_array': self.ruler_array,
            'start_point_y': self.start_point_y,
            'start_point_x': self.start_point_x,
            'ruler_self': ruler_self,
            'ruler_enemy': ruler_enemy,
            'enemy_chosen_color': self.chosen_color
        }
        self.request(self.now_turn(), info_dict)

    def initialize_arrays(self):  # Initialize arrays if new round starts.
        for y in range(self.height):
            for x in range(self.width):
                self.color_array[y][x] = self.shared_dict['color_array_init'][y][x]
                self.ruler_array[y][x] = 0

    def absorb(self, ruler, chosen_color):
        for y in range(self.height):  # Fill ruled area with chosen_color.
            for x in range(self.width):
                if self.ruler_array[y][x] == ruler:
                    self.color_array[y][x] = chosen_color

        absorb_repeat = True
        while absorb_repeat:  # Absorb repeatedly for complete absorbing.
            for y in range(self.height):  # Copy ruler_array for repetitive absorbing.
                for x in range(self.width):
                    self.ruler_array_copy[y][x] = self.ruler_array[y][x]

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
                    if self.ruler_array[y][x] != self.ruler_array_copy[y][x]:
                        absorb_repeat = True
                        check_stop = True  # To escape from outer for loop.
                        break

    def check_status(self):
        self.score[self.round] = [0, 0]
        finish = True
        for y in range(self.height):
            for x in range(self.width):
                if self.ruler_array[y][x] == 0:
                    finish = False
                elif self.ruler_array[y][x] == 1:
                    self.score[self.round][0] += 1
                elif self.ruler_array[y][x] == 2:
                    self.score[self.round][1] += 1
        return finish


class PixelsFinishPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsFinishPhase, self).__init__(logic_server, message_type)

        # Initialize variables from outside.
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()

        # Initialize variables.
        self.cnt_player = 2

    def on_start(self):
        super(PixelsFinishPhase, self).on_start()
        logging.debug('PixelsFinishPhase.on_start')

    def do_action(self, pid, dict_data):
        super(PixelsFinishPhase, self).do_action(pid, dict_data)
        logging.debug('PixelsLoopPhase.do_action')
        logging.debug('pid : ' + pid)

        self.cnt_player -= 1

        if self.cnt_player == 0:
            score = self.shared_dict['score']
            #ruler 0
            ruler0 = score[0][0] + score[1][0]
            #ruler 1
            ruler1 = score[0][1] + score[1][1]

            if ruler0 > ruler1:
                win = 0
                lose = 1
            elif ruler0 < ruler1:
                win = 1
                lose = 0
            else:
                win = 2
                lose = 2


            logging.error(pid + ' **************************')
            send_dict = {'win': win,
                         'lose': lose,
                         'ruler0_score': ruler0,
                         'ruler1_score': ruler1}

            self.notify_winner(send_dict)
            self.end(True, send_dict)
            return


    def on_end(self):
        super(PixelsFinishPhase, self).on_end()
        logging.debug('PixelsFinishPhase.on_end')

    def notify_winner(self, winner_dict):
        notify_dict = winner_dict
        self.notify(notify_dict)

    def send_game_over(self):
        logging.debug('Send gameover message to ' + self.now_turn())
        self.request(self.now_turn(), {})


class PixelsGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(PixelsGameLogic, self).__init__(game_server)
        logging.debug('GameLogic : INIT')

        # Initialize constants.
        self.width = 128
        self.height = 96
        # Width and height must be multiples of 8.
        # Because start_point of rulers are 3/8 and 5/8 points of board.
        self.num_of_color = 6

        # Declare color_array_init.
        self.color_array_init = [[0 in range(self.width)] in range(self.height)]

        # Initialize start_point.
        self.start_point_y = [self.height / 8 * 3 - 1, self.height / 8 * 5]
        self.start_point_x = [self.width / 8 * 3 - 1, self.width / 8 * 5]
        # If width or height = 8, [2, 5] (0 ~ 7)
        # If width or height = 80, [29, 50] (0 ~ 79)

    def on_start(self, player_list):
        super(PixelsGameLogic, self).on_start(player_list)
        logging.debug('GameLogic : ON_START')

        # Initialize the color_array_init with random color 1 ~ 6.
        for y in range(self.height):
            for x in range(self.width):
                self.color_array_init[y][x] = random.randint(1, self.num_of_color)

        # Let the colors of start_points 0.
        self.color_array_init[self.start_point_y[0]][self.start_point_x[0]] = 0
        self.color_array_init[self.start_point_y[1]][self.start_point_x[1]] = 0

        # shared_dict for initialized board
        shared_dict = self.get_shared_dict()
        shared_dict['width'] = self.width
        shared_dict['height'] = self.height
        shared_dict['color_array_init'] = self.color_array_init
        shared_dict['start_point_y'] = self.start_point_y
        shared_dict['start_point_x'] = self.start_point_x

        loop_phase = PixelsLoopPhase(self, 'loop')
        finish_phase = PixelsFinishPhase(self, 'finish')

        shared_dict['PHASE_LOOP'] = self.append_phase(loop_phase)
        shared_dict['PHASE_FINISH'] = self.append_phase(finish_phase)

        self.change_turn(0)

        logging.debug('PixelsGameLogic -> LoopPhase')
        self.change_phase(0)
