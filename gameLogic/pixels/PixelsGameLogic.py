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

# {"msg":"game_data","msg_type": 정할거,"data":정할거}

class PixelsLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsLoopPhase, self).__init__(logic_server, message_type)

    def on_start(self):
        super(PixelsLoopPhase, self).on_start()
        logging.debug('PixelsLoopPhase.on_start')
        self.player_list = self.get_player_list()
        shared_dict = self.get_shared_dict()

    def do_action(self, pid, dict_data):
        super(PixelsLoopPhase, self).do_action(pid, dict_data)
        logging.debug('PixelsLoopPhase.do_action')
        logging.debug('pid : ' + pid)

    def on_end(self):
        super(PixelsLoopPhase, self).on_end()
        logging.debug('PixelsLoopPhase.on_end')




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
        self.color_array = [[0 for x in range(self.width)] for y in range(self.height)]
        self.ruler_array = [[0 for x in range(self.width)] for y in range(self.height)]

        # Set up the map (random color 1 ~ 6)
        for y in range(self.height):
            for x in range(self.width):
                self.color_array[y][x] = random.randint(1, self.num_of_color)

        # Set up start_point
        self.start_point = [[3 / 8 * self.height, 3 / 8 * self.width],
                            [5 / 8 * self.height, 5 / 8 * self.width]]

        # Let the colors of start_points 0.
        self.color_array[self.start_point[0][0]][self.start_point[0][1]] = 0
        self.color_array[self.start_point[1][0]][self.start_point[1][1]] = 0

        # shared_dict for initialized map
        shared_dict = self.get_shared_dict()
        shared_dict['color_array'] = self.color_array
        shared_dict['ruler_array'] = self.ruler_array
        shared_dict['start_point'] = self.start_point

        loop_phase = PixelsLoopPhase(self, 'loop')
        finish_phase = PixelsFinishPhase(self, 'finish')

        shared_dict['PHASE_LOOP'] = self.append_phase(loop_phase)
        shared_dict['PHASE_FINISH'] = self.append_phase(finish_phase)

        self.change_turn(0)

        logging.debug('PixelsGameLogic -> LoopPhase')
        self.change_phase(0)