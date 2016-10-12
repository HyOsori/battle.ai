import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic
from gameLogic.baseClass.Phase import Phase
import logging
import random
logging.basicConfig(level=logging.DEBUG)

'''
ShardDict Key

PHASE_LOOP -> 'loop'->
PHASE_FINISH -> 'finish'->
board
'''

class PixelsLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsLoopPhase, self).__init__(logic_server, message_type)


    def on_start(self):
        super(PixelsLoopPhase, self).on_start()
        logging.debug('PixelsLoopPhase.on_start')
        self.player_list = self.get_player_list()
        shared_dict = self.get_shared_dict()

        self.round = 0  # To check whether phase must be changed or not
        self.initialize = False  # To initialize arrays when new round starts.
        self.turn = 0  # To record the turns of a round.

        self.score_amount = [0, 0]  # To record the amounts of scores.
        self.score = [0, 0] # To record the scores of each round.

        # Set up variables from shared_dict
        self.width = shared_dict['width']
        self.height = shared_dict['height']

        # Set up the arrays
        self.color_array = [[0 for x in range(self.width)] for y in range(self.height)]
        self.ruler_array = [[0 for x in range(self.width)] for y in range(self.height)]
        self.ruler_array_copy = [[0 for x in range(self.width)] for y in range(self.height)]

        # Copy the arrays
        self.initialize_arrays()


    def do_action(self, pid, dict_data):
        super(PixelsLoopPhase, self).do_action(pid, dict_data)
        logging.debug('PixelsLoopPhase.do_action')
        logging.debug('pid : ' + pid)

        if (self.round == 2):
            pass

        if (self.initialize):
            self.initialize_arrays()
            self.score_amount = self.score
            self.score = [0, 0]
            self.initialize = False

        ruler = 0
        if (pid == self.player_list[0]):
            ruler = 1
            self.turn = self.turn + 1
        if (pid == self.player_list[1]):
            ruler = 2
        chosen_color = dict_data['chosen_color']

        self.absorb(ruler, chosen_color)

        if (self.check_status()):
            self.round = self.round + 1
            self.initialize = True


    def on_end(self):
        super(PixelsLoopPhase, self).on_end()
        logging.debug('PixelsLoopPhase.on_end')


    def initialize_arrays(self):
        shared_dict = self.get_shared_dict()
        for y in range(self.height):
            for x in range(self.width):
                self.color_array[y][x] = shared_dict['color_array_init'][y][x]


    def absorb(self, ruler, chosen_color):
        for y in range(self.height):  # Fill ruled area with chosen_color
            for x in range(self.width):
                if (self.ruler_array[y][x] == ruler):
                    self.color_array[y][x] = chosen_color

        absorb_repeat = True
        while (absorb_repeat):  # For complete absorbing
            for y in range(self.height):  # Copy ruler_array for complete absorbing
                for x in range(self.width):
                    self.ruler_array_copy[y][x] = self.ruler_array[y][x]

            for y in range(self.height):  # Absorb
                for x in range(self.width):
                    if (self.ruler_array[y][x] == 0 and self.color_array[y][x] == chosen_color and (
                            # If the area isn't ruled and is filled with chosen color
                                        (x > 0 and self.ruler_array[y][x - 1] == ruler) or  # Check left side
                                        (x < (self.width - 1) and self.ruler_array[y][x + 1] == ruler) or  # Check right side
                                    (y > 0 and self.ruler_array[y - 1][x] == ruler) or  # Check up side
                                (y < (self.height - 1) and self.ruler_array[y + 1][x] == ruler))):  # Check down side
                        self.ruler_array[y][x] = ruler  # Rule the area

            absorb_repeat = False
            check_stop = False
            for y in range(self.height):  # If ruler_array == ruler_array_copy -> Finish absorbing.
                if (check_stop):
                    break
                for x in range(self.width):
                    if (self.ruler_array[y][x] != self.ruler_array_copy[y][x]):
                        absorb_repeat = True;
                        check_stop = True  # For escape from outer for loop.
                        break


    def check_status(self):
        self.score = [0, 0]
        finish = True
        for y in range(self.height):
            for x in range(self.width):
                if (self.ruler_array[y][x] == 0):
                    finish = False
                elif (self.ruler_array[y][x] == 1):
                    self.score[0] = self.score[0] + 1
                elif (self.ruler_array[y][x] == 2):
                    self.score[1] = self.score[1] + 1
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

    def on_start(self, player_list):
        logging.debug('PixelsGameLogic.on_start')
        super(PixelsGameLogic, self).on_start(player_list)

        # Width and height must be multiples of 8.
        # Because start_point of players are 3/8 and 5/8 points of map.
        self.width = 128
        self.height = 96
        self.num_of_color = 6

        # Set up the arrays
        self.color_array_init = [[0 for x in range(self.width)] for y in range(self.height)]
        self.ruler_array_init = [[0 for x in range(self.width)] for y in range(self.height)]

        # Set up the map (random color 1 ~ 6)
        for y in range(self.height):
            for x in range(self.width):
                self.color_array[y][x] = random.randint(1, self.num_of_color)

        # Set up start_point
        self.start_point = [[3 / 8 * self.height, 3 / 8 * self.width],
                            [5 / 8 * self.height, 5 / 8 * self.width]]

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