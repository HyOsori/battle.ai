#-*- coding:utf-8 -*-
from tornado import queues, gen
import json
from server.string import *

import server.debugger as logging

"""
GameServer (for all games, abstract class)

"""


class GameHandler:
    def __init__(self, room, players, observers, game_logic, time_index=4, database=None):
        self.game_logic = game_logic
        self.room = room
        self.pid_list = [p.get_pid() for p in self.room.player_list]
        self.players = players  # WHY NEEDED? - when game room destroy - player added in list
        self.observers = observers  # WHY NEEDED? - when game room destroy - attendee.notify_user_added
        self.q = None

        self.time_delay_list = [1, 0.7, 0.5, 0.3, 0.2]

        self.delay_time = 0.3
        self.set_delay_time(self.time_delay_list[time_index])

        self.game_result = {}
        self.error_msg = "none"

        self.current_msg_type = "start"
        self.error_code = 1
        self.normal_game_playing = True
        self.turns = []

        self.round_result = None
        self.game_end = False

        self.score = [0, 0, 0]

        self.database = database

        # self.game_log_manager = GameLogManager()

    @gen.coroutine
    def game_handler(self, round_num = 0):
        '''
        Handle game playing

        :param round_num: number of round to play game
        '''

        self.turns = self._select_turns(self.room.player_list)
        # TODO: round num is set by server ? y / n

        self.q = queues.Queue(len(self.room.player_list))
        for turn in self.turns:
            # check game normal flag
            if not self.normal_game_playing:
                break

            logging.info("=====Are You Ready=====" + str(turn))
            ready = yield self.__ready_check(self.room.player_list)
            logging.debug("ready status : " + str(ready))
            if not ready:
                return

            logging.info("=====Game Start=====" + str(turn))
            self.game_logic.on_start(turn)

            for player in self.room.player_list:
                self.q.put(player)
                self._play_handler(player)
            yield self.q.join()
            logging.info("=====Game End=====" + str(turn))
        yield self.destroy_room()
        logging.info("=====Destroy Room=====" + str(self.turns[0]))

    def _select_turns(self, players):
        turn = [player.get_pid() for player in players]
        #print len(turn)
        #new_turn = self.perm(turn, 0, len(turn))
        #print new_turn

        return [turn, [turn[1], turn[0]]]

    @gen.coroutine
    def __ready_check(self, players):

        # init setting
        self.round_result = None
        self.game_end = False

        # send Are you ready message
        return_flag = True
        cur_player = None
        msg = {MSG: GAME_HANDLER, MSG_TYPE: READY, DATA: {}}
        try:
            data = json.dumps(msg)
            for player in players:
                cur_player = player
                player.send(data)
                recv_data = yield player.read()
                recv_msg = json.loads(recv_data)
                if not recv_msg[DATA][RESPONSE] == 'OK':
                    return_flag = False
                    raise gen.Return(False)
            # recv Are you ready message

            # send web that all player ready OK
            recv_msg[DATA] = {RESPONSE_: OK, PLAYERS: [player.get_pid() for player in players]}
            data = json.dumps(recv_msg)
            for attendee in self.room.attendee_list:
                attendee.send(data)
            return_flag = True
            raise gen.Return(True)
        except Exception as e:
            if return_flag:
                raise gen.Return(True)
            for p in self.room.player_list:
                if not p.get_pid() == cur_player.get_pid():
                    self.players[p.get_pid()] = p
            raise gen.Return(False)

    def _error_handler(self):
        pass

    def _play_handler(self, player):
        '''
        handle player's game playing
        :param player: player object
        '''
        raise NotImplementedError

    def request(self, pid, msg_type, data):
        # TODO: in this function, read data from client is needed
        '''
        callback function
        game logic call this function to request player's response
        :param pid: player id
        :param msg_type: message type
        :param data: message data
        '''

        for p in self.room.player_list:
            if p.get_pid() == pid:
                player = p
                break

        self.current_msg_type = msg_type

        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        json_data = json.dumps(message)

        player.send(json_data)

        # TODO: implementation of read data in here
        # return data or save data in self var ?

    def notify(self, msg_type, data):
        '''
        callback function
        game logic call this function to notify game data
        :param msg_type: notifying message
        :param data: message data
        '''
        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        json_data = json.dumps(message)

        for player in self.room.player_list:
            player.send(json_data)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

    def on_end(self, is_valid_end, message):
        """
        callback function
        when game is ended this function is called by GameLogic
        :param is_valid_end: 0 (normal end), 1 (abnormal end)
        :param message: game result information
        """

        self.game_result = message

        if is_valid_end:
            self.game_end = True
            message = {MSG: GAME_DATA, MSG_TYPE: ROUND_RESULT, DATA: message}
            self.round_result = message
        else:
            # temporary implementation
            if message[self.pid_list[0]] == "win":
                self.score[0] += 1
            else:
                self.score[1] += 1
            logging.debug("logic error occured")
            raise Exception

        json_data = json.dumps(message)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

    def send_round_result(self, round_result):
        # save round result, temporary implementation ..;;
        try:
            if not bool(round_result[DATA]["draw"]):
                tmp_l = self.pid_list
                self.score[tmp_l.index(round_result[DATA]["winner"])] += 1

            self.current_msg_type = ROUND_RESULT
            json_data = json.dumps(round_result)
        except Exception as e:
            logging.error(e.message)
            json_data = "error"

        for player in self.room.player_list:
            player.send(json_data)

    @gen.coroutine
    def destroy_room(self):
        '''
        When all round is ended, room is destroyed. Clients get back to robby.
        '''
        # TODO: game_result must chagned to real game_result, not round result

        # make game result, temporary implementation.. ;;
        # TODO: result = { "pid1" : score, "pid2" : score, "error_code": (num) }
        # error_code : 0 - success, 1 - logic_error, 2 - timeout_error, 3 - unexpected error
        result = {}
        try:
            result[self.pid_list[0]] = self.score[0]
            result[self.pid_list[1]] = self.score[1]
            if not self.normal_game_playing:
                result[ERROR_CODE] = 1
            else:
                result[ERROR_CODE] = 0
        except Exception as e:
            logging.error(e.message)

        # game_log_manager.add_game_log(info1[0], info1[1], info2[0], info2[1], info1[1] == info2[1])
        # game_log_manager.print_all()

        data = {MSG: GAME_HANDLER, MSG_TYPE: GAME_RESULT, DATA: result}

        logging.debug(data)

        json_data = json.dumps(data)

        # temporary implemenation ;; must be del
        if self.normal_game_playing:
            for player in self.room.player_list:
                player.send(json_data)

            for player in self.room.player_list:
                yield player.read()

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

        for player in self.room.player_list:
            # temporary implementation
            if player.get_pid() == 'Dummy3':
                continue
            self.players[player.get_pid()] = player
            for attendee in self.observers.values():
                attendee.notice_user_added(player.get_pid())

    def set_delay_time(self, delay_time=0.1):
        self.delay_time = delay_time

    @gen.coroutine
    def delay_action(self):
        yield gen.sleep(self.delay_time)

    def save_game_data(self):
        pass

    def _exit_handler(self, player):
        logging.error("** exit error handler **")
        self.game_logic.on_error(player.get_pid())
        self.normal_game_playing = False

        for pid in self.pid_list:
            if pid == player.get_pid():
                self.room.player_list.remove(player)
            logging.error("task_done call!")
            self.q.get()
            self.q.task_done()

        # temporary implementation ;; must be del
        result = {}
        try:
            result[self.pid_list[0]] = self.score[0]
            result[self.pid_list[1]] = self.score[1]
            if not self.normal_game_playing:
                result[ERROR_CODE] = 1
            else:
                result[ERROR_CODE] = 0
        except Exception as e:
            logging.error(e.message)

        data = {MSG: GAME_HANDLER, MSG_TYPE: GAME_RESULT, DATA: result}
        self.current_msg_type = GAME_RESULT

        for p in self.room.player_list:
            logging.error("[!!]" + str(data))
            p.send(json.dumps(data))

        gen.Return(None)



