import sys

from gamebase.game.Phase import Phase
from gamebase.game.TurnGameLogic import TurnGameLogic
import game.debugger as logging
import math

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
        self.player_pos = []

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

            pos = [[0 for _ in range(2)] for _ in range(5)]
            for i_row in range(self.count):
                pos[i_row][0] = i_row * 20 + 10
                pos[i_row][1] = color_count * 80 + 10

            self.player_pos += pos
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

        self.array_egg = [Egg for _ in range(10)]

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
            self.array_egg[i] = Egg(self.player_pos[i][0], self.player_pos[i][1], 0)
        for i in range(self.count, self.count * 2):
            self.array_egg[i] = Egg(self.player_pos[i][0], self.player_pos[i][1], 1)

        # Send server msg
        self.change_turn(0)
        self.request_to_server(0, 0, [0.0, 0.0], 0)

    def do_action(self, pid, dict_data):

        index = dict_data['index']
        direction = dict_data['direction']
        force = dict_data['force']

        # validate_user
        validate_user = 0
        if pid == self.player_list[0]:
            validate_user = 0
        elif pid == self.player_list[1]:
            validate_user = 1
            index += self.count

        # 형 변환후 힘 넣기
        self.array_egg[index].add_force(direction[0], direction[1], force)

        self.run_physics()

        self.change_turn()
        # Notify to Observer(Web) game data
        self.notify_to_observer(validate_user, 0, [0.6, 0.4], 4)
        # Requests to Server(Handler) game data
        self.request_to_server(validate_user, 0, [0.6, 0.4], 4)

    def run_physics(self):
        # 충돌 체크
        for i in range(len(self.array_egg)):
            if self.array_egg[i].speed > 0:
                my_speed = self.array_egg[i].speed()
                my_x_dir = self.array_egg[i].x_dir()
                my_y_dir = self.array_egg[i].y_dir()

                self.array_egg[i].x_pos += my_x_dir * my_speed
                self.array_egg[i].y_pos += my_y_dir * my_speed
                self.array_egg[i].speed -= 0.1

                for j in range(len(self.array_egg)):
                    check_meet = False
                    if j is not i:
                        while (self.is_meet(self.array_egg[i].x_pos, self.array_egg[i].y_pos,
                                            self.array_egg[j].x_pos, self.array_egg[j].y_pos)):
                            if not check_meet:
                                check_meet = True

                            if self.array_egg[i].x_pos > self.array_egg[j].x_pos:
                                self.array_egg[i].x_pos += math.fabs(self.array_egg[i].x_dir)
                            else:
                                self.array_egg[i].x_pos -= math.fabs(self.array_egg[i].x_dir)

                            if self.array_egg[i].y_pos > self.array_egg[j].y_pos:
                                self.array_egg[i].y_pos += math.fabs(self.array_egg[i].y_dir)
                            else:
                                self.array_egg[i].y_pos -= math.fabs(self.array_egg[i].y_dir)

                        if check_meet:
                            kiss_dir_x = self.array_egg[j].x_pos - self.array_egg[i].x_pos
                            kiss_dir_y = self.array_egg[j].y_pos - self.array_egg[i].y_pos
                            distance = math.sqrt(kiss_dir_x * kiss_dir_x + kiss_dir_y * kiss_dir_y)

                            self.array_egg[j].x_dir = kiss_dir_x / distance
                            self.array_egg[j].y_dir = kiss_dir_y / distance

                            cos_b = float(self.array_egg[i].x_dir * self.array_egg[j].x_dir
                                          + self.array_egg[i].y_dir * self.array_egg[j].y_dir)
                            cos_a = float(math.sqrt(1 - math.fabs(cos_b)))

                            if 0 < int(cos_a * 10000) < 1:
                                cos_a = 0.0001
                            elif -1 < int(cos_a * 10000) < 0:
                                cos_a = -0.0001

                            if 0 < int(cos_b * 10000) < 1:
                                cos_b = 0.0001
                            elif -1 < int(cos_b * 10000) < 0:
                                cos_b = -0.0001

                            self.array_egg[i].x_dir -= self.array_egg[j].x_dir * cos_b
                            self.array_egg[i].y_dir -= self.array_egg[j].y_dir * cos_b

                            self.array_egg[j].speed = self.array_egg[i].speed * \
                                (1 / (cos_a * cos_a / cos_b + cos_b))
                            self.array_egg[i].speed = self.array_egg[j].speed * \
                                (1 / (cos_b * cos_b / cos_a + cos_a))

        check_remain_energy = False
        for i in range(len(self.array_egg)):
            if self.array_egg[i].speed > 0:
                check_remain_energy = True
                break

        if check_remain_energy:
            self.run_physics()

    def is_meet(self, x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        if distance <= self.radius * 2:
            return True
        return False

    def notify_to_observer(self, turn, index, direction, force):
        notify_dict = {
            'turn': turn,
            'index': index,
            'direction': direction,
            'force': force
        }
        self.notify("game", notify_dict)

    def request_to_server(self, turn, index, direction, force):
        logging.info('Request ' + self.now_turn() + '\'s decision')
        request_dict = {
            'turn': turn,
            'index': index,
            'direction': direction,
            'force': force
        }
        self.request(self.now_turn(), request_dict)


class Egg:
    x_pos = None
    y_pos = None
    color = None
    x_dir = None
    y_dir = None
    speed = None

    def __init__(self, x_pos, y_pos, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.x_dir = 0
        self.y_dir = 0
        self.speed = 0

    def add_force(self, x_dir, y_dir, speed):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.speed = speed
