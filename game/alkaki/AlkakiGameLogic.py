import sys

from gamebase.game.Phase import Phase
from gamebase.game.TurnGameLogic import TurnGameLogic
import game.debugger as logging

sys.path.insert(0, '../')


class ALKAKIGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(ALKAKIGameLogic, self).__init__(game_server)
        # board_size (width height)
        # count Egg for each player
        # circle radius
        # Position Egg
        self.board_size = 100
        self.count = 5
        self.radius = 1
        self.player_pos = [0 for col in range(2)]

        # Here init game dependent variable

    def on_ready(self, player_list):
        self._player_list = player_list

        # Here makes dict for multi player init variable

        init_dict = {}
        color_count = 0

        for i in player_list:
            init_dict[i] = {}
            init_dict[i]['board_size'] = self.board_size
            init_dict[i]['count'] = self.count
            init_dict[i]['radius'] = self.radius
            init_dict[i]['color'] = color_count

            pos = [[0 for col in range(2)] for row in range(self.count)]
            for i_row in range(self.count):
                pos[i_row][0] = i_row * 20 + 10
                pos[i_row][1] = color_count * 80 + 10

            self.player_pos[color_count] = pos
            init_dict[i]['player_pos'] = pos
            color_count += 1

        # Send Server
        self._game_server.on_init_game(init_dict)

    def on_start(self):
        # shared_dict-init out of this class(Phase)
        shared_dict = self.get_shared_dict()

        shared_dict['board_size'] = self.board_size
        shared_dict['count'] = self.count
        shared_dict['radius'] = self.radius
        shared_dict['player_pos'] = self.player_pos

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
        self.player_list = None
        self.shared_dict = None


        # Init game independent data
        self.board_size = None
        self.count = None
        self.radius = None
        self.player_pos = None
        self.color = None

        self.array_egg = [[0 for col in range(5)] for row in range(2)]


    def do_start(self):
        logging.info("do_start")
        # Init data
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()

        # Init game independent data
        self.board_size = self.shared_dict['board_size']
        self.count = self.shared_dict['count']
        self.radius = self.shared_dict['radius']
        self.player_pos = self.shared_dict['player_pos']

        for i in range(self.count):
            self.array_egg[0][i] = Egg(self.player_pos[0][i][0], self.player_pos[0][i][0])
        for i in range(self.count):
            self.array_egg[1][i] = Egg(self.player_pos[1][i][0], self.player_pos[1][i][1])

        # Send server msg
        self.change_turn(0)
        self.request_to_server(0, [0.0, 0.0], 0)

    def do_action(self, pid, dict_data):
        # validate_user
        validate_user = 0
        if pid == self.player_list[0]:
            validate_user = 0
        elif pid == self.player_list[1]:
            validate_user = 1

        index = dict_data['index']
        direction = dict_data['direction']
        force = dict_data['force']


        self.change_turn()
        # Notify to Observer(Web) game data
        self.notify_to_observer(0, [0.6, 0.4], 4)
        # Requests to Server(Handler) game data
        self.request_to_server(0, [0.6, 0.4], 4)

    def notify_to_observer(self, index, direction, force):
        notify_dict = {
            'index': index,
            'direction': direction,
            'force' :force
        }
        self.notify("game", notify_dict)

    def request_to_server(self, index, direction, force):
        logging.info('Request ' + self.now_turn() + '\'s decision')
        request_dict = {
            'index': index,
            'direction': direction,
            'force' :force
        }
        self.request(self.now_turn(), request_dict)

class Egg:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_dir = 0
        self.y_dir = 0
        self.speed = 0

    def add_force(self, x_dir, y_dir, force):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.speed = force
