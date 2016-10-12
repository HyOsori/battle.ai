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
'''


class PixelsLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsLoopPhase, self).__init__(logic_server, message_type)

        logging.debug('PHASE_LOOP : INIT')

        # Initialize variables from outside.
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()
        self.next_phase = self.shared_dict['PHASE_FINISH']
        self.width = self.shared_dict['width']
        self.height = self.shared_dict['height']

        # Initialize variables.
        self.round = 0  # Check Rounds.
        self.initialize = False  # Initialize arrays when new round starts.
        self.score = [[0, 0], [0, 0]]  # Record the scores of two rounds.
        self.chosen_color = 0

        # Use these arrays in the form of 'array[y][x]'.
        self.color_array = [[0 in range(self.width)] in range(self.height)]
        self.color_array_old = [[0 in range(self.width)] in range(self.height)]
        # Copy color_array to notify front_end of the change in map.
        self.ruler_array = [[0 in range(self.width)] in range(self.height)]
        self.ruler_array_copy = [[0 in range(self.width)] in range(self.height)]
        # Copy ruler_array for complete absorbing at absorb().

    def on_start(self):
        super(PixelsLoopPhase, self).on_start()
        logging.debug('PHASE_LOOP : START')

        # Pycharm recommends us not to define instance attribute outside __init__.

        # Copy the arrays
        self.initialize_arrays()

    def do_action(self, pid, dict_data):
        super(PixelsLoopPhase, self).do_action(pid, dict_data)
        logging.debug('PHASE_LOOP : DO_ACTION / pid : ' + pid)

        if self.initialize:
            self.initialize_arrays()
            self.score[self.round] = [0, 0]
            self.initialize = False

        if self.round == 2:  # go to next phase
            self.shared_dict['score'] = self.score
            self.change_phase(self.next_phase)

        ruler = 0
        if pid == self.player_list[0]:
            ruler = 1
        if pid == self.player_list[1]:
            ruler = 2
        self.chosen_color = dict_data['chosen_color']

        #
        for y in range(self.height):
            for x in range(self.width):
                self.color_array_old[y][x] = self.color_array[y][x]

        self.absorb(ruler, self.chosen_color)

        if self.check_status():
            self.round += 1
            self.initialize = True

        self.request_to_client()
        self.notify_to_front()

    def on_end(self):
        super(PixelsLoopPhase, self).on_end()
        logging.debug('PixelsLoopPhase.on_end')

    def notify_to_front(self):
        notify_dict = {
            'width': self.width,
            'height': self.height,
            'color_array_old': self.color_array_old,
            'color_array': self.color_array,
            'ruler_array': self.ruler_array,
            'score': self.score
        }
        self.notify(notify_dict)

    def request_to_client(self):
        logging.debug('Request ' + self.now_turn() + '\'s decision')
        info_dict = {
            'width': self.width,
            'height': self.height,
            'color_array': self.color_array,
            'ruler_array': self.ruler_array,
            'chosen_color': self.chosen_color
        }
        self.request(self.now_turn(), info_dict)

    def initialize_arrays(self):  # Initialize arrays when new round starts.
        for y in range(self.height):
            for x in range(self.width):
                self.color_array[y][x] = self.shared_dict['color_array_init'][y][x]

    def absorb(self, ruler, chosen_color):
        for y in range(self.height):  # Fill ruled area with chosen_color
            for x in range(self.width):
                if self.ruler_array[y][x] == ruler:
                    self.color_array[y][x] = chosen_color

        absorb_repeat = True
        while absorb_repeat:  # For complete absorbing
            for y in range(self.height):  # Copy ruler_array for complete absorbing
                for x in range(self.width):
                    self.ruler_array_copy[y][x] = self.ruler_array[y][x]

            for y in range(self.height):  # Absorb
                for x in range(self.width):
                    if self.ruler_array[y][x] == 0 and self.color_array[y][x] == chosen_color and (
                        # If the area isn't ruled and is filled with chosen color
                        (x > 0 and self.ruler_array[y][x - 1] == ruler) or  # Check left side
                        (x < (self.width - 1) and self.ruler_array[y][x + 1] == ruler) or  # Check right side
                        (y > 0 and self.ruler_array[y - 1][x] == ruler) or  # Check up side
                        (y < (self.height - 1) and self.ruler_array[y + 1][x] == ruler)
                    ):  # Check down side
                        self.ruler_array[y][x] = ruler  # Rule the area

            absorb_repeat = False
            check_stop = False
            for y in range(self.height):  # If ruler_array == ruler_array_copy -> Finish absorbing.
                if check_stop:
                    break
                for x in range(self.width):
                    if self.ruler_array[y][x] != self.ruler_array_copy[y][x]:
                        absorb_repeat = True;
                        check_stop = True  # For escape from outer for loop.
                        break

    def check_status(self):
        self.score = [0, 0]
        finish = True
        for y in range(self.height):
            for x in range(self.width):
                if self.ruler_array[y][x] == 0:
                    finish = False
                elif self.ruler_array[y][x] == 1:
                    self.score[0] += 1
                elif self.ruler_array[y][x] == 2:
                    self.score[1] += 1
        return finish


class PixelsFinishPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsFinishPhase, self).__init__(logic_server, message_type)

    def on_start(self):
        super(PixelsFinishPhase, self).on_start()
        logging.debug('PixelsFinishPhase.on_start')

    def do_action(self, pid, dict_data):
        super(PixelsLoopPhase, self).do_action(pid, dict_data)
        logging.debug('PixelsLoopPhase.do_action')
        logging.debug('pid : ' + pid)

    def on_end(self):
        super(PixelsFinishPhase, self).on_end()
        logging.debug('PixelsFinishPhase.on_end')


class PixelsGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(PixelsGameLogic, self).__init__(game_server)

        # Width and height must be multiples of 8.
        # Because start_point of players are 3/8 and 5/8 points of map.
        self.width = 128
        self.height = 96
        self.num_of_color = 6

        # Set up the arrays
        self.color_array_init = [[0 in range(self.width)] in range(self.height)]
        self.ruler_array_init = [[0 in range(self.width)] in range(self.height)]

        # Set up start_point
        self.start_point = [[3 / 8 * self.height, 3 / 8 * self.width],
                            [5 / 8 * self.height, 5 / 8 * self.width]]

    def on_start(self, player_list):
        logging.debug('PixelsGameLogic.on_start')
        super(PixelsGameLogic, self).on_start(player_list)

        # Set up the map (random color 1 ~ 6)
        for y in range(self.height):
            for x in range(self.width):
                self.color_array[y][x] = random.randint(1, self.num_of_color)

        # Let the colors of start_points 0.
        self.color_array_init[self.start_point[0][0]][self.start_point[0][1]] = 0
        self.color_array_init[self.start_point[1][0]][self.start_point[1][1]] = 0

        # shared_dict for initialized map
        shared_dict = self.get_shared_dict()
        shared_dict['width'] = self.width
        shared_dict['height'] = self.height
        shared_dict['color_array_init'] = self.color_array_init
        shared_dict['ruler_array_init'] = self.ruler_array_init
        shared_dict['start_point'] = self.start_point

        loop_phase = PixelsLoopPhase(self, 'loop')
        finish_phase = PixelsFinishPhase(self, 'finish')

        shared_dict['PHASE_LOOP'] = self.append_phase(loop_phase)
        shared_dict['PHASE_FINISH'] = self.append_phase(finish_phase)

        self.change_turn(0)

        logging.debug('PixelsGameLogic -> LoopPhase')
        self.change_phase(0)
