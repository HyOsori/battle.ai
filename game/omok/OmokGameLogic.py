import base64
import json
import random
import sys
import zlib

from gamebase.game.Phase import Phase

from gamebase.game.TurnGameLogic import TurnGameLogic

import game.debugger as logging

sys.path.insert(0, '../')
#logging.basicConfig(level=logging.DEBUG)

class OmokGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(OmokGameLogic, self).__init__(game_server)
        logging.debug('GameLogic : INIT')
        self.width = 5
        self.height = 5

        # Declare color_array_init.
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

    def on_ready(self, pid_list):
        init_dict = {}
        color_count = 0;
        self._player_list = pid_list

        self._result_dict = dict(
            zip(self._player_list, ['draw'] * len(self._player_list))
        )
        self._turn_num = -1
        self.change_turn()

        for i in pid_list:
            color_count += 1
            init_dict[i] = {}
            init_dict[i]["width"] = self.width
            init_dict[i]["height"] = self.width
            init_dict[i]["color"] = color_count

        logging.debug(init_dict)
        self._game_server.on_init_game(init_dict)

    def on_start(self):
        logging.debug('GameLogic : ON_START')

        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

        # shared_dict for initialized board
        shared_dict = self.get_shared_dict()

        loop_phase = OmokLoopPhase(self, 'loop')
        finish_phase = OmokFinishPhase(self, 'finish')

        shared_dict['PHASE_LOOP'] = self.append_phase(loop_phase)
        shared_dict['PHASE_FINISH'] = self.append_phase(finish_phase)

        self.change_turn(0)

        logging.debug('OmokGameLogic -> LoopPhase')
        self.change_phase(0)

    def end(self, error_code ,result):
        self._game_server.on_end(error_code, result)


class OmokLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(OmokLoopPhase, self).__init__(logic_server, message_type)
        logging.debug('PHASE_LOOP : INIT')

        #game data
        self.width = 5
        self.height = 5

        # Declare color_array_init.
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

    def on_start(self):
        super(OmokLoopPhase, self).on_start()
        logging.debug('PHASE_LOOP : START')

        # Initialize variables from outside.
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()
        self.next_phase = self.shared_dict['PHASE_FINISH']
        #self.width = self.shared_dict['width']
        #self.height = self.shared_dict['height']
        #self.board = self.shared_dict['board']



        # Initialize variables.
        self.round = 0  # Check Rounds.
        self.initialize = False  # Initialize arrays if new round starts.

        #self.notify_to_front_init()

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



        x_pos = dict_data["x"]
        y_pos = dict_data["y"]

        result = self.check_game_end(ruler, x_pos, y_pos)
        if result["type"] == 1:
            # Normal flow
            pass
        elif result["type"] == 0:
            # [WIN] complete omok
            self.end(0, {"winner": result["winner"]})
        elif result["type"] == 100:
            # [WIN] put again same board
            self.end(100, {"winner": result["winner"]})
        elif result["type"] == 101:
            # [DRAW] all board filled
            self.end(101, {"winner": 0})

        if result["type"] != 1:
            return

            #self.end(0, {"winner": self.player_list[0]})

        self.notify_to_front()  # send web

        logging.debug(dict_data)

        if self.initialize:  # Initialize the arrays if new(2nd) round starts.
             self.board = [[0 for x in range(self.width)] for y in range(self.height)]
             self.initialize = False

             if pid == self.player_list[1]:
                 self.change_turn()
        #
        # if self.round == 2:  # Change phase if two rounds are finished.
        #     self.shared_dict['score'] = self.score
        #     # logging.debug('LoopPhase -> FinishPhase')
        #     self.change_phase(self.next_phase)
        #     return
        #

        ruler_enemy = ruler  # Ruler who finished absorbing
        ruler_self = ruler % 2 + 1  # Ruler who will take the request

        self.change_turn()
        self.request_to_client(ruler_self, ruler_enemy)

    def on_end(self, result):
        super(OmokLoopPhase, self).on_end(0, result)
        # logging.debug('PHASE LOOP : ON_END')

    def notify_to_front(self):
        notify_dict = {
            'board': self.board
        }
        self.notify("string", notify_dict)

    def notify_to_front_change_round(self):
        print('notify to front end round')
        notify_dict = {
            'round': self.round,
            'first': self.player_list[self.round],
            'second': self.player_list[1 - self.round]
        }
        self.notify_free('notify_change_round', notify_dict)
    """
    def request_to_client(self, ruler_self, ruler_enemy):
        # logging.debug('Request ' + self.now_turn() + '\'s decision')
        info_dict = {
            'ruler_self': ruler_self,
            'ruler_enemy': ruler_enemy,
            'enemy_chosen_location': self.chosen_location
        }
        self.request(self.now_turn(), info_dict)
    """

    def request_to_client(self, ruler_self, ruler_enemy):
        logging.debug('Request ' + self.now_turn() + '\'s decision')
        info_dict = {
            'board': self.board
        }
        self.request(self.now_turn(), info_dict)

    def check_game_end(self, color, x_pos, y_pos):
        # 정상종료나 에러아무거나 나오면 Finish Phase
        if self.board[x_pos][y_pos] != 0:
            # TYPE 100 이미 있는 곳에 돌을 놨다!
            return {"type": 100, "winner": (color - 3)}
        else:
            self.board[x_pos][y_pos] = color
            if self.check_omok(color, x_pos, y_pos):
                # TYPE 0 5목 완성!
                return {"type": 0, "winner": color}

        for i in range(self.width):
            for j in range(self.height):
                # TYPE 1 자리가 남아있어서 노말진행!
                if self.board[i][j] == 0:
                    return {"type": 1}

        # TYPE 101 모든돌이 꽉 찼다!
        return {"type": 101}

    def check_omok(self, color, xPos, yPos):
        if self.add_omok(color, xPos, yPos, -1, -1) + self.add_omok(color, xPos, yPos, 1, 1) == 4:
            return True
        if self.add_omok(color, xPos, yPos, 0, -1) + self.add_omok(color, xPos, yPos, 0, 1) == 4:
            return True
        if self.add_omok(color, xPos, yPos, 1, -1) + self.add_omok(color, xPos, yPos, -1, 1) == 4:
            return True
        if self.add_omok(color, xPos, yPos, -1, 0) + self.add_omok(color, xPos, yPos, 1, 0) == 4:
            return True

    def add_omok(self, color, x_pos, y_pos, x_dir, y_dir):
        if x_pos + x_dir < 0:
            return 0
        if x_pos + x_dir > self.width - 1:
            return 0
        if y_pos + y_dir < 0:
            return 0
        if y_pos + y_dir > self.height - 1:
            return 0

        if self.board[x_pos + x_dir][y_pos + y_dir] == color:
            return 1 + self.add_omok(color, x_pos + x_dir, y_pos + y_dir, x_dir, y_dir)
        else:
            return 0




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

