import math
import sys

from game.base.TurnGameLogic import TurnGameLogic

import utils.debugger as logging
from game.base.Phase import Phase

sys.path.insert(0, '../')

FRICTION = 100

class ALKAKIGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(ALKAKIGameLogic, self).__init__(game_server)
        # board_size (width height)
        # count Egg for each player
        # circle radius
        # Position Egg
        # Here init game dependent variable
        try:
            self.board_size = 100000
            self.count = 5
            self.radius = 3000
            self.player_pos = []
        except Exception as e:
            logging.info(e)
            logging.info("[Error] init_variable_error")
            self.end(101, None)
            return

    def on_ready(self, player_list):
        try:
            self._player_list = player_list
        except Exception as e:
            logging.info(e)
            logging.info("[Error] get_player_list_error")
            self.end(130, None)
            return

        # Here makes dict for multi player init variable
        init_dict = {}
        try:
            color_count = 0

            for i in player_list:
                init_dict[i] = {}
                init_dict[i]['board_size'] = self.board_size
                init_dict[i]['count'] = self.count
                init_dict[i]['radius'] = self.radius
                init_dict[i]['color'] = color_count

                pos = [[0 for _ in range(2)] for _ in range(5)]
                for i_row in range(self.count):
                    pos[i_row][0] = int((i_row + 1) * 47000 / 3 + 3000)
                    pos[i_row][1] = int(color_count * 47000 * 4 / 3 + 3000 + (49000 / 3))

                self.player_pos += pos
                init_dict[i]['player_pos'] = pos
                color_count += 1
        except Exception as e:
            logging.info(e)
            logging.info("[Error] set_init_dict_using_init_variable_error")
            self.end(102, None)
            return

        # Send Server
        try:
            self._game_server.on_init_game(init_dict)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] set_init_dict_using_init_variable_error")
            self.end(160, None)
            return

    def on_start(self):
        # shared_dict-init out of this class(Phase)
        shared_dict = self.get_shared_dict()
        try:
            shared_dict['board_size'] = self.board_size
            shared_dict['count'] = self.count
            shared_dict['radius'] = self.radius
            shared_dict['player_pos'] = self.player_pos
        except Exception as e:
            logging.info(e)
            logging.info("[Error] set_shared_dict_to_send_other_phase_error")
            self.end(103, None)
            return

        try:
            # Register Phase (phase name free)
            game_phase = ALKAKIGamePhase(self, 'game')
            shared_dict['PHASE_GAME'] = self.append_phase(game_phase)
            # Transfer Phase GameLogic -> GamePhase
            self.change_phase(0)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] change_phase_error")
            self.end(105, None)
            return


class ALKAKIGamePhase(Phase):
    def __init__(self, logic_server, message_type):
        super(ALKAKIGamePhase, self).__init__(logic_server, message_type)
        try:
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
        except Exception as e:
            logging.info(e)
            logging.info("[Error] init_variable_error")
            self.end(101, None)
            return

    def do_start(self):
        logging.info("do_start")
        # Init data
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()

        try:
            # Init game independent data
            self.board_size = self.shared_dict['board_size']
            self.count = self.shared_dict['count']
            self.radius = self.shared_dict['radius']
            self.player_pos = self.shared_dict['player_pos']

            for i in range(self.count):
                self.array_egg[i] = Egg(self.player_pos[i][0], self.player_pos[i][1], 0)
            for i in range(self.count, self.count * 2):
                self.array_egg[i] = Egg(self.player_pos[i][0], self.player_pos[i][1], 1)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] get_shared_dict_error")
            self.end(104, None)
            return

        try:
            # Send server msg
            self.change_turn(0)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] change_turn_error")
            self.end(106, None)
            return

        try:
            # self.request_to_server(0, 0, [0.0, 0.0], 0)
            self.request_to_server(0, self.array_egg)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] request_to_server_error")
            self.end(162, None)
            return

    def do_action(self, pid, dict_data):
        index = None
        direction = None
        force = None

        try:
            index = dict_data['index']
            direction = dict_data['direction']
            force = int(dict_data['force'])
        except Exception as e:
            logging.info(e)
            logging.info("[Error] get_game_dict_data_error")
            self.end(131, None)
            return

        # validate_user
        validate_user = 0
        try:
            if pid == self.player_list[0]:
                validate_user = 0
            elif pid == self.player_list[1]:
                validate_user = 1
                index += self.count
        except Exception as e:
            logging.info(e)
            logging.info("[Error] get_game_dict_data_error")
            self.end(107, None)
            return

        # 형 변환후 힘 넣기
        is_game_end = None
        # 0~n 까지중 죽은거 무시
        # 5~n 까지중 죽은거 무시

        i_validate_arr = validate_user * 5
        my_count = index - i_validate_arr
        for i in range(5):
            if self.array_egg[i_validate_arr + i].alive:
                if my_count == 0:
                    index += i
                    break
                else:
                    my_count -= 1

        if index < i_validate_arr or index > i_validate_arr + 5:
            logging.info("error occured by array in 205line")

        try:
            direction = list(map(int, direction))
            distance = int(math.sqrt(direction[0] ** 2 + direction[1] ** 2))

            x_dir = direction[0] / distance
            y_dir = direction[1] / distance
            # TODO : direction < 1 죽여
            self.array_egg[index].add_force(x_dir, y_dir, force)

        except Exception as e:
            logging.info(e)
            logging.info("[Error] user_game_error")
            self.end(180, None)
            return

        try:
            self.run_physics()
        except Exception as e:
            logging.info(e)
            logging.info("[Error] user_game_error")
            self.end(182, None)
            return

        try:
            is_game_end = self.check_game_end()
        except Exception as e:
            logging.info(e)
            logging.info("[Error] user_game_error")
            self.end(183, None)
            return


        # for i in range(10):
        #     logging.info(self.array_egg[i].x_pos)

        try:
            # Notify to Observer(Web) game data
            self.notify_to_observer(validate_user, index - i_validate_arr, [direction[0], direction[1]], force)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] notify_to_observer_error")
            self.end(161, None)
            return

        try:
            if is_game_end["type"] == "win":
                self.end(0, {'winner': is_game_end['person']})
                return
            elif is_game_end["type"] == "draw":
                self.end(1, {'winner': is_game_end['person']})
                return
            elif is_game_end["type"] == "play":
                pass

        except Exception as e:
            logging.info(e)
            logging.info("[Error] send server to End Error")

        try:
            self.change_turn()
        except Exception as e:
            logging.info(e)
            logging.info("[Error] change_turn_error")
            self.end(106, None)
            return

        try:
            # Requests to Server(Handler) game data
            #self.request_to_server(validate_user, 0, [direction[0], direction[1]], force)
            self.request_to_server(validate_user, self.array_egg)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] request_to_server_error")
            self.end(162, None)
            return

    def run_physics(self):
        # 충돌 체크
        for i in range(len(self.array_egg)):
            if self.array_egg[i].speed > 0 and self.array_egg[i].alive:

                my_speed = self.array_egg[i].speed
                my_x_dir = self.array_egg[i].x_dir
                my_y_dir = self.array_egg[i].y_dir

                self.array_egg[i].x_pos += int(my_x_dir * my_speed)
                self.array_egg[i].y_pos += int(my_y_dir * my_speed)
                self.array_egg[i].speed -= FRICTION

                for j in range(len(self.array_egg)):
                    check_meet = False
                    if j is not i and self.array_egg[j].alive:

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

                            if cos_b == 0:
                                self.array_egg[j].speed = 0
                            else:
                                self.array_egg[j].speed = self.array_egg[i].speed * \
                                    (1 / (cos_a * cos_a / cos_b + cos_b))

                            if cos_a == 0:
                                self.array_egg[i].speed = 0
                            else:
                                self.array_egg[i].speed = self.array_egg[j].speed * \
                                    (1 / (cos_b * cos_b / cos_a + cos_a))

        check_remain_energy = False
        for i in range(len(self.array_egg)):
            if self.array_egg[i].speed > 0 and self.array_egg[i].alive:
                check_remain_energy = True
                break

        for i in range(len(self.array_egg)):
            if self.array_egg[i].x_pos < 0 or self.array_egg[i].x_pos > 100000 or \
                            self.array_egg[i].y_pos < 0 or self.array_egg[i].y_pos > 100000:
                self.array_egg[i].alive = False

        if check_remain_energy:
            self.run_physics()

    def is_meet(self, x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        if distance <= self.radius * 2:
            return True
        return False

    def check_game_end(self):
        array_dead_list = []
        array_alive_list = []
        game_end = False
        for index_pid in range(len(self.player_list)):

            pid = self.player_list[index_pid]
            count = 0

            # 죽은 돌 전부 세기
            for i in range(self.count):
                logging.info(self.array_egg[(index_pid * self.count) + i].alive)
                if not self.array_egg[(index_pid * self.count) + i].alive:
                    count = count + 1
            if count == self.count:
                array_dead_list.append(pid)
                game_end = True
            else:
                array_alive_list.append(pid)

        if game_end:
            if len(array_dead_list) == 1:
                return {
                    "type": "win",
                    "person": array_alive_list
                }
            elif len(array_dead_list) == len(self.player_list):
                return {
                    "type": "draw",
                    "person": array_dead_list
                }

        return {
            "type": "play"
        }

    def notify_to_observer(self, turn, index, direction, force):
        notify_dict = {
            'turn': turn,
            'index': index,
            'direction': direction,
            'force': force
        }
        self.notify("game", notify_dict)

    def request_to_server(self, index, array):
        logging.info('Request ' + self.now_turn() + '\'s decision')
        # 내가 0일때 나 0~4 적 5~9
        my_cnt = 0
        enemy_cnt = 0

        for i in range(5):
            if array[index * 5 + i].alive:
                my_cnt += 1
            if array[(1-index) * 5 + i].alive:
                enemy_cnt += 1

        my_arr = [[0 for _ in range(2)] for _ in range(my_cnt)]
        enemy_arr = [[0 for _ in range(2)] for _ in range(enemy_cnt)]

        my_cnt = 0
        enemy_cnt = 0

        for i in range(5):
            if array[index * 5 + i].alive:
                my_arr[my_cnt][0] = array[index * 5 + i].x_pos
                my_arr[my_cnt][1] = array[index * 5 + i].y_pos
                my_cnt += 1
            if array[(1-index) * 5 + i].alive:
                enemy_arr[enemy_cnt][0] = array[(1-index) * 5 + i].x_pos
                enemy_arr[enemy_cnt][1] = array[(1-index) * 5 + i].y_pos
                enemy_cnt += 1

        # 내가 1일때 나 5~9 적 0~4
        request_dict = {
            'index': index,
            'my_arr': my_arr,
            'enemy_arr': enemy_arr
        }
        self.request(self.now_turn(), request_dict)

class Egg:
    x_pos = None
    y_pos = None
    color = None
    x_dir = None
    y_dir = None
    speed = None
    alive = None

    def __init__(self, x_pos, y_pos, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.x_dir = 0
        self.y_dir = 0
        self.speed = 0
        self.alive = True

    def add_force(self, x_dir, y_dir, speed):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.speed = speed
