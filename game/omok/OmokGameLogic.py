import sys

from gamebase.game.Phase import Phase

from gamebase.game.TurnGameLogic import TurnGameLogic

import game.debugger as logging

sys.path.insert(0, '../')


class OMOKGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(OMOKGameLogic, self).__init__(game_server)
        logging.debug('GameLogic : INIT')
        self.width = 5
        self.height = 5
        self.board = [[0 for x in range(self.width)] for y in range(self.height)]

    def on_ready(self, pid_list):
        self._player_list = pid_list

        # -1 : yet Init state
        self._turn_num = -1

        # Send Game Data To Server
        init_dict = {}
        color_count = 0
        for i in pid_list:
            color_count += 1
            init_dict[i] = {}
            init_dict[i]['width'] = self.width
            init_dict[i]['height'] = self.width
            init_dict[i]['color'] = color_count

        # logging.debug(init_dict)
        self._game_server.on_init_game(init_dict)

    def on_start(self):
        logging.debug('GameLogic : ON_START')

        # shared_dict for Initialize in Phase(Loop, Finish)
        shared_dict = self.get_shared_dict()
        shared_dict['width'] = self.width
        shared_dict['height'] = self.height
        shared_dict['board'] = self.board

        # Register Phase
        loop_phase = OMOKLoopPhase(self, 'loop')
        shared_dict['PHASE_LOOP'] = self.append_phase(loop_phase)

        # Move Loop Phase
        logging.debug('OMOKGameLogic -> LoopPhase')
        self.change_phase(0)


class OMOKLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(OMOKLoopPhase, self).__init__(logic_server, message_type)
        logging.debug('PHASE_LOOP : INIT')

        # game data
        self.player_list = None
        self.shared_dict = None
        self.width = None
        self.height = None
        self.board = None

    def on_start(self):
        super(OMOKLoopPhase, self).on_start()
        logging.debug('PHASE_LOOP : START')

        # Init data
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()

        # Init game independent data
        self.width = self.shared_dict['width']
        self.height = self.shared_dict['height']
        self.board = self.shared_dict['board']

        self.change_turn(0)
        self.request_to_client()

    def do_action(self, pid, dict_data):
        super(OMOKLoopPhase, self).do_action(pid, dict_data)
        # logging.debug('PHASE_LOOP : DO_ACTION / pid : ' + pid)

        # Validate User
        validate_user = 0
        if pid == self.player_list[0]:
            validate_user = 1
        if pid == self.player_list[1]:
            validate_user = 2

        # Player Action
        x_pos = dict_data['x']
        y_pos = dict_data['y']
        logging.debug(dict_data)

        # Check Valid Action
        result = self.check_game_end(validate_user, x_pos, y_pos)

        # Send to Front
        self.notify_to_front()

        # Check Game End(normal, error)
        if result['type'] == 1:
            # Normal flow
            pass
        elif result['type'] == 0:
            # [WIN] complete game
            self.end(0, {'winner': result['winner']})
        elif result['type'] == 100:
            # [WIN] put again same board
            self.end(100, {"winner": result['winner']})
        elif result["type"] == 101:
            # [DRAW] all board filled
            self.end(101, {"winner": 0})

        # abnormal End Occur!
        if result["type"] != 1:
            return

        # normal Flow
        self.change_turn()
        self.request_to_client()

    def notify_to_front(self):
        notify_dict = {
            'board': self.board
        }
        self.notify("loop", notify_dict)

    def request_to_client(self):
        logging.debug('Request ' + self.now_turn() + '\'s decision')
        info_dict = {
            'board': self.board
        }
        self.request(self.now_turn(), info_dict)

    # ================== Check Game Play ================== #
    def check_game_end(self, color, x_pos, y_pos):
        # 정상종료나 에러아무거나 나오면 Finish Phase
        if self.board[x_pos][y_pos] != 0:
            # TYPE 100 이미 있는 곳에 돌을 놨다!
            return {"type": 100, "winner": (color - 3)}
        else:
            self.board[x_pos][y_pos] = color

            if self.check_five(color, x_pos, y_pos):

                # TYPE 0 5목 완성!
                return {"type": 0, "winner": color}

        for i in range(self.width):
            for j in range(self.height):
                # TYPE 1 자리가 남아있어서 노말진행!
                if self.board[i][j] == 0:
                    return {"type": 1}

        # TYPE 101 모든돌이 꽉 찼다!
        return {"type": 101}

    def check_five(self, color, x_pos, y_pos):
        if self.add_one(color, x_pos, y_pos, -1, -1) + self.add_one(color, x_pos, y_pos, 1, 1) == 4:
            return True
        if self.add_one(color, x_pos, y_pos, 0, -1) + self.add_one(color, x_pos, y_pos, 0, 1) == 4:
            return True
        if self.add_one(color, x_pos, y_pos, 1, -1) + self.add_one(color, x_pos, y_pos, -1, 1) == 4:
            return True
        if self.add_one(color, x_pos, y_pos, -1, 0) + self.add_one(color, x_pos, y_pos, 1, 0) == 4:
            return True

    def add_one(self, color, x_pos, y_pos, x_dir, y_dir):
        if x_pos + x_dir < 0:
            return 0
        if x_pos + x_dir > self.width - 1:
            return 0
        if y_pos + y_dir < 0:
            return 0
        if y_pos + y_dir > self.height - 1:
            return 0

        if self.board[x_pos + x_dir][y_pos + y_dir] == color:
            return 1 + self.add_one(color, x_pos + x_dir, y_pos + y_dir, x_dir, y_dir)
        else:
            return 0
    # ===================================================== #

