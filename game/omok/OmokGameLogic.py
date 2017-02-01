import base64
import json
import logging
import random
import sys
import zlib

from gamebase.game.Phase import Phase

from gamebase.game.TurnGameLogic import TurnGameLogic

sys.path.insert(0, '../')
logging.basicConfig(level=logging.DEBUG)

class OmokGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(OmokGameLogic, self).__init__(game_server)
        logging.debug('GameLogic : INIT')

        # Declare color_array_init.
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

    def on_start(self, player_list):
        super(OmokGameLogic, self).on_start(player_list)
        logging.debug('GameLogic : ON_START')

        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

        # shared_dict for initialized board
        shared_dict = self.get_shared_dict()
        shared_dict['width'] = self.width
        shared_dict['height'] = self.height
        shared_dict['board'] = self.board

        loop_phase = OmokLoopPhase(self, 'loop')
        finish_phase = OmokFinishPhase(self, 'finish')

        shared_dict['PHASE_LOOP'] = self.append_phase(loop_phase)
        shared_dict['PHASE_FINISH'] = self.append_phase(finish_phase)

        self.change_turn(0)

        logging.debug('OmokGameLogic -> LoopPhase')
        self.change_phase(0)

class OmokLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(OmokLoopPhase, self).__init__(logic_server, message_type)
        logging.debug('PHASE_LOOP : INIT')

        def on_start(self):
            super(OmokLoopPhase, self).on_start()
            logging.debug('PHASE_LOOP : START')

            # Initialize variables from outside.
            self.player_list = self.get_player_list()
            self.shared_dict = self.get_shared_dict()
            self.next_phase = self.shared_dict['PHASE_FINISH']
            self.width = self.shared_dict['width']
            self.height = self.shared_dict['height']
            self.board = self.shared_dict['board']

            # Initialize variables.
            self.round = 0  # Check Rounds.
            self.initialize = False  # Initialize arrays if new round starts.

            self.notify_to_front_init()

            self.change_turn(0)
            self.request_to_client(1, 2)

        def do_action(self, pid, dict_data):
            super(OmokLoopPhase, self).do_action(pid, dict_data)
            # logging.debug('PHASE_LOOP : DO_ACTION / pid : ' + pid)

            ruler = 0
            if pid == self.player_list[0]:
                ruler = 1
            if pid == self.player_list[1]:
                ruler = 2

            if self.chosen_location == dict_data['chosen_location']:
                result = dict(zip(self.player_list, ['win'] * len(self.player_list)))
                result[pid] = 'lose'
                logging.error(pid + ' invalid Chosen')
                self.end(False, result)
                return

            self.absorb(ruler, self.chosen_color)
            self.notify_to_front(ruler)

            if self.check_status():  # If check_status returns True, the round is finished.
                self.notify_to_front_change_round()
                self.round += 1

                self.initialize = True

            if self.initialize:  # Initialize the arrays if new(2nd) round starts.
                self.board = [[0 for x in range(self.width)] for y in range(self.height)]
                self.initialize = False

                if pid == self.player_list[1]:
                    self.change_turn()

            if self.round == 2:  # Change phase if two rounds are finished.
                self.shared_dict['score'] = self.score
                # logging.debug('LoopPhase -> FinishPhase')
                self.change_phase(self.next_phase)
                return

            ruler_enemy = ruler  # Ruler who finished absorbing
            ruler_self = ruler % 2 + 1  # Ruler who will take the request

            self.change_turn()
            self.request_to_client(ruler_self, ruler_enemy)

        def on_end(self):
            super(OmokLoopPhase, self).on_end()
            # logging.debug('PHASE LOOP : ON_END')

        def notify_to_front_init(self):
            notify_dict = {
                'width': self.width,
                'height': self.height,
                'board': json.dumps(self.board)
            }
            self.notify_init(notify_dict)

        def notify_to_front(self, ruler):
            notify_dict = {
                'ruler_who': ruler,  # Who just finished absorbing
                'chosen_location': self.chosen_location,
                'score': self.score
            }
            self.notify(notify_dict)

        def notify_to_front_change_round(self):
            print('notify to front end round')
            notify_dict = {
                'round': self.round,
                'first': self.player_list[self.round],
                'second': self.player_list[1 - self.round]
            }
            self.notify_free('notify_change_round', notify_dict)

        def request_to_client(self, ruler_self, ruler_enemy):
            # logging.debug('Request ' + self.now_turn() + '\'s decision')
            info_dict = {
                'ruler_self': ruler_self,
                'ruler_enemy': ruler_enemy,
                'enemy_chosen_location': self.chosen_location
            }
            self.request(self.now_turn(), info_dict)

        def absorb(self, ruler, location):
            return



class OmokFinishPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(OmokFinishPhase, self).__init__(logic_server, message_type)
        logging.debug('PHASE_FINISH : INIT')

    def on_start(self):
        super(OmokFinishPhase, self).on_start()
        logging.debug('PHASE_FINISH : ON_START')

        # Initialize variables from outside.
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()

        # Initialize variables.
        self.cnt_player = 2

        self.change_turn(0)
        self.send_game_over()

    def do_action(self, pid, dict_data):
        super(OmokFinishPhase, self).do_action(pid, dict_data)
        logging.debug('PHASE_FINISH : DO_ACTION / pid : ' + pid)

        self.cnt_player -= 1

        if self.cnt_player == 0:

            score = self.shared_dict['score']
            # ruler 1
            ruler1 = score[0] + score[0]
            # ruler 2
            ruler2 = score[1] + score[1]

            winner = 'DRAW'
            draw = False

            if ruler1 > ruler2:
                winner = self.player_list[0]
            elif ruler1 < ruler2:
                winner = self.player_list[1]
            else:
                draw = True

            logging.error(pid + ' **************************')
            send_dict = {
                         'winner': winner,
                         'score': score,
                         'draw': draw
                        }
            print('winner', winner, 'score', score)
            self.notify_winner(send_dict)
            self.end(True, send_dict)
            return

        self.change_turn()
        self.send_game_over()

    def on_end(self):
        super(OmokFinishPhase, self).on_end()
        logging.debug('PHASE_FINISH : ON_END')

    def notify_winner(self, winner_dict):
        notify_dict = winner_dict
        self.notify(notify_dict)

    def send_game_over(self):
        logging.debug('Send gameover message to ' + self.now_turn())
        self.request(self.now_turn(), {'empty':0})

