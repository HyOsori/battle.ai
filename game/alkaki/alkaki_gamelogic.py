import math
import sys

from game.base.TurnGameLogic import TurnGameLogic

import utils.debugger as logging
from game.base.Phase import Phase

sys.path.insert(0, '../')

FRICTION = 100
BOARD_SIZE = 100000
EGG_COUNT = 5
EGG_RADIUS = 3000

STR_BOARD_SIZE = "board_size"
STR_COUNT = "count"
STR_RADIUS = "radius"
STR_COLOR = "color"
STR_FRICTION = "friction"

STR_PLAYER_POS = "player_pos"

STR_INDEX = "index"
STR_FORCE = "force"
STR_DIRECTION = "direction"
STR_TURN = "turn"
STR_TYPE = "type"

STR_MY_ARR = "my_arr"
STR_ENEMY_ARR = "enemy_arr"

def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def is_egg_crush(egg1, egg2):
    distance = get_distance(egg1.x_pos, egg1.y_pos, egg2.x_pos, egg2.y_pos)
    return distance <= EGG_RADIUS * 2   # diameter of egg


class ALKAKIGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(ALKAKIGameLogic, self).__init__(game_server)
        # board_size (width height)
        # count Egg for each player
        # circle radius
        # Position Egg
        # Here init game dependent variable
        try:
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
                init_dict[i] = dict()
                init_dict[i][STR_BOARD_SIZE] = BOARD_SIZE
                init_dict[i][STR_COUNT] = EGG_COUNT
                init_dict[i][STR_RADIUS] = EGG_RADIUS
                init_dict[i][STR_FRICTION] = FRICTION
                init_dict[i][STR_COLOR] = color_count

                pos = [[0 for _ in range(2)] for _ in range(5)]
                for i_row in range(EGG_COUNT):
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
            shared_dict[STR_BOARD_SIZE] = BOARD_SIZE
            shared_dict[STR_COUNT] = EGG_COUNT
            shared_dict[STR_RADIUS] = EGG_RADIUS
            shared_dict[STR_PLAYER_POS] = self.player_pos
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
            self.player_pos = None
            self.color = None

            self.array_egg = [None for _ in range(EGG_COUNT * 2)]
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
            self.player_pos = self.shared_dict[STR_PLAYER_POS]

            for i in range(EGG_COUNT):
                self.array_egg[i] = Egg(self.player_pos[i][0], self.player_pos[i][1], 0)
            for i in range(EGG_COUNT, EGG_COUNT * 2):
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
        try:
            index = dict_data[STR_INDEX]
            direction = dict_data[STR_DIRECTION]
            force = int(dict_data[STR_FORCE])
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
                index += EGG_COUNT
        except Exception as e:
            logging.info(e)
            logging.info("[Error] get_game_dict_data_error")
            self.end(107, None)
            return

        # 0~n 까지중 죽은거 무시
        # 5~n 까지중 죽은거 무시

        i_validate_arr = validate_user * EGG_COUNT
        my_count = index - i_validate_arr
        for i in range(EGG_COUNT):
            if self.array_egg[i_validate_arr + i].alive:
                if my_count == 0:
                    index += i
                    break
                else:
                    my_count -= 1

        if index < i_validate_arr or index > i_validate_arr + 5:
            logging.info("error occured by array in 205line")

        try:
            # TODO: can be problem
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

        try:
            self.notify_to_observer(validate_user, index - i_validate_arr, [direction[0], direction[1]], force)
        except Exception as e:
            logging.info(e)
            logging.info("[Error] notify_to_observer_error")
            self.end(161, None)
            return

        try:
            if is_game_end[STR_TYPE] == "win":
                self.end(0, {'winner': is_game_end['person']})
                return
            elif is_game_end[STR_TYPE] == "draw":
                self.end(1, {'winner': is_game_end['person']})
                return
            elif is_game_end[STR_TYPE] == "play":
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
        for cur_egg in self.array_egg:
            if cur_egg.speed <= 0 or not cur_egg.alive:
                continue

            # TODO: can be problem
            cur_egg.x_pos += int(cur_egg.x_dir * cur_egg.speed)
            cur_egg.y_pos += int(cur_egg.y_pos * cur_egg.speed)
            cur_egg.speed -= FRICTION

            for cmp_egg in self.array_egg:
                check_meet = False

                if (cmp_egg is cur_egg) or not cmp_egg.alive:
                    continue

                while is_egg_crush(cur_egg, cmp_egg):
                    check_meet = True

                    if cur_egg.x_pos > cmp_egg.x_pos:
                        cur_egg.x_pos += abs(cur_egg.x_dir)
                    else:
                        cur_egg.x_pos -= abs(cur_egg.x_dir)

                    if cur_egg.y_pos > cmp_egg.y_pos:
                        cur_egg.y_pos += abs(cur_egg.y_dir)
                    else:
                        cur_egg.y_pos -= abs(cur_egg.y_dir)

                if not check_meet:
                    continue

                kiss_dir_x = cmp_egg.x_pos - cur_egg.x_pos
                kiss_dir_y = cmp_egg.y_pos - cur_egg.y_pos
                distance = math.sqrt(kiss_dir_x ** 2 + kiss_dir_y ** 2)

                cmp_egg.x_dir = kiss_dir_x / distance
                cmp_egg.y_dir = kiss_dir_y / distance

                # TODO: ask dude - what the calc --
                cos_b = cur_egg.x_dir * cmp_egg.x_dir + cur_egg.y_dir * cmp_egg.y_dir
                cos_a = math.sqrt(1 - math.fabs(cos_b))

                if 0 < int(cos_a * 10000) < 1:
                    cos_a = 0.0001
                elif -1 < int(cos_a * 10000) < 0:
                    cos_a = -0.0001

                if 0 < int(cos_b * 10000) < 1:
                    cos_b = 0.0001
                elif -1 < int(cos_b * 10000) < 0:
                    cos_b = -0.0001

                cur_egg.x_dir -= cmp_egg.x_dir * cos_b
                cur_egg.y_dir -= cmp_egg.y_dir * cos_b

                if cos_b == 0:
                    cmp_egg.speed = 0
                else:
                    cmp_egg.speed = cur_egg.speed * (1 / (cos_a * cos_a / cos_b + cos_b))

                if cos_a == 0:
                    cur_egg.speed = 0
                else:
                    cur_egg.speed = cmp_egg.speed * (1 / (cos_b * cos_b / cos_a + cos_a))
                # TODO: ...

        check_remain_energy = False

        for cur_egg in self.array_egg:
            if cur_egg.speed > 0 and cur_egg.alive:
                check_remain_energy = True
                break
        for cur_egg in self.array_egg:
            if not (0 < cur_egg.x_pos < BOARD_SIZE and 0 < cur_egg.y_pos < BOARD_SIZE):
                cur_egg.alive = False

        if check_remain_energy:
            self.run_physics()

    def check_game_end(self):
        array_dead_list = []
        array_alive_list = []
        game_end = False
        for index, pid in enumerate(self.player_list):
            count = 0

            # 죽은 돌 전부 세기
            for i in range(EGG_COUNT):
                logging.info(self.array_egg[(index * EGG_COUNT) + i].alive)
                if not self.array_egg[(index * EGG_COUNT) + i].alive:
                    count += 1
            if count == EGG_COUNT:
                array_dead_list.append(pid)
                game_end = True
            else:
                array_alive_list.append(pid)

        if game_end:
            if len(array_dead_list) == 1:
                return {"type": "win", "person": array_alive_list}
            elif len(array_dead_list) == len(self.player_list):
                return {"type": "draw", "person": array_dead_list}
        return {"type": "play"}

    def notify_to_observer(self, turn, index, direction, force):
        notify_dict = {
            STR_TURN: turn,
            STR_INDEX: index,
            STR_DIRECTION: direction,
            STR_FORCE: force
        }
        self.notify("game", notify_dict)

    def request_to_server(self, index, array):
        logging.info('Request ' + self.now_turn() + '\'s decision')
        # 내가 0일때 나 0~4 적 5~9
        my_cnt = 0
        enemy_cnt = 0

        for i in range(EGG_COUNT):
            if array[index * EGG_COUNT + i].alive:
                my_cnt += 1
            if array[(1-index) * EGG_COUNT + i].alive:
                enemy_cnt += 1

        my_arr = [[0 for _ in range(2)] for _ in range(my_cnt)]
        enemy_arr = [[0 for _ in range(2)] for _ in range(enemy_cnt)]

        my_cnt = 0
        enemy_cnt = 0

        for i in range(EGG_COUNT):
            if array[index * EGG_COUNT + i].alive:
                my_arr[my_cnt][0] = array[index * EGG_COUNT + i].x_pos
                my_arr[my_cnt][1] = array[index * EGG_COUNT + i].y_pos
                my_cnt += 1
            if array[(1-index) * EGG_COUNT + i].alive:
                enemy_arr[enemy_cnt][0] = array[(1-index) * EGG_COUNT + i].x_pos
                enemy_arr[enemy_cnt][1] = array[(1-index) * EGG_COUNT + i].y_pos
                enemy_cnt += 1

        # 내가 1일때 나 5~9 적 0~4
        request_dict = {
            STR_INDEX: index,
            STR_MY_ARR: enemy_arr,
            STR_ENEMY_ARR: my_arr
        }
        self.request(self.now_turn(), request_dict)


class Egg:
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
