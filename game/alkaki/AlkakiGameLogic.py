import sys

from gamebase.game.Phase import Phase
from gamebase.game.TurnGameLogic import TurnGameLogic
import game.debugger as logging

sys.path.insert(0, '../')


class ALKAKIGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(ALKAKIGameLogic, self).__init__(game_server)
        self.board_size = 18
        self.count = 4
        self.pos = []

        # Here init game dependent variable

    def on_ready(self, player_list):
        self._player_list = player_list

        # Here makes dict for multi player init variable
        init_dict = {}
        color_count = 0
        for i in player_list:
            init_dict[i] = {}
            init_dict[i]['board_size'] = 18
            init_dict[i]['count'] = 4
            for i in range(self.count):

            # init_dict[i]['pos'] = color_count
            color_count += 1

        # Send Server
        self._game_server.on_init_game(init_dict)

    def on_start(self):
        # shared_dict-init out of this class(Phase)
        shared_dict = self.get_shared_dict()
        # Register Phase (phase name free)
        game_phase = ALKAKIGamePhase(self, 'game')
        shared_dict['PHASE_GAME'] = self.append_phase(game_phase)
        # Transfer Phase GameLogic -> GamePhase
        self.change_phase(0)


class ALKAKIGamePhase(Phase):
    def __init__(self, logic_server, message_type):
        super(ALKAKIGamePhase, self).__init__(logic_server, message_type)

        # declare variable
        self.player_list = None
        self.shared_dict = None

        # Init data
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()

        # Init game independent data

    def do_start(self):
        # Send server msg
        self.change_turn(0)
        self.request_to_server()

    def do_action(self, pid, dict_data):
        logging.info("do_action called")
        # validate_user
        validate_user = 0
        if pid == self.player_list[0]:
            validate_user = 1
        elif pid == self.player_list[1]:
            validate_user = 2

        self.change_turn()
        # Notify to Observer(Web) game data
        self.notify_to_observer()
        # Requests to Server(Handler) game data
        self.request_to_server()

    def notify_to_observer(self):
        notify_dict = {
            'data': 'test'
        }
        self.notify("game", notify_dict)

    def request_to_server(self):
        logging.info('Request ' + self.now_turn() + '\'s decision')
        request_dict = {
            'data': 'test'
        }
        self.request(self.now_turn(), request_dict)
