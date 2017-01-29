# -*- coding:utf-8 -*-
from tornado import queues, gen
import json
from server.string import *

import server.debugger as logging

"""
GameServer (for all games, abstract class)

"""


class GameHandler:
    def __init__(self, room, players, observers, game_logic, time_index=4, database=None):
        self.game_logic = game_logic  # TODO: rename ...
        self.room = room  # player objects and observer objects are in here
        self.pid_list = [p.get_pid() for p in self.room.player_list]
        self.players = players  # WHY NEEDED? - when game room destroy - player added in list
        self.observers = observers  # WHY NEEDED? - when game room destroy - attendee.notify_user_added

        self.time_delay_list = [1, 0.7, 0.5, 0.3, 0.2]

        self.delay_time = 0.3
        self.set_delay_time(self.time_delay_list[time_index])

        self.game_result = {}
        self.error_msg = "none"

        self.current_msg_type = "start"  # TODO: remove
        self.error_code = 1  # TODO: specify error code
        self.normal_game_playing = True
        self.turns = []  # TODO: remove

        self.round_result = None  # TODO: remove
        self.game_end = False

        self.score = [0, 0, 0]  # TODO: remove

        self.database = database  # TODO: db setting is needed

        self.played = None  # player currently finished turn

        # self.game_log_manager = GameLogManager()

    @gen.coroutine
    def run(self):
        '''
        Handle game playing

        :param round_num: number of round to play game
        '''

        # TODO: round num is set by server ? y / n

        # check game normal flag
        # if not self.normal_game_playing:
        #     break

        # logging.info("=====Are You Ready=====")
        # ready = yield self.__ready_check(self.room.player_list)
        # logging.debug("ready status : " + str(ready))
        # if not ready:
        #     return

        logging.info("=====Game Start=====")
        # self.game_logic.on_start(turn)

        yield self._play_handler(None)

        logging.info("=====Game End=====")
        self.destroy_room()
        logging.info("=====Destroy Room=====")

    def _select_turns(self, players):
        turn = [player.get_pid() for player in players]
        # print len(turn)
        # new_turn = self.perm(turn, 0, len(turn))
        # print new_turn

        return [turn, [turn[1], turn[0]]]

    # TODO: current code ,,, this function is skipped. insert it into current code flow and fixup it.
    @gen.coroutine
    def __ready_check(self, players):
        '''
        socket connection valid check
        and communication with front_end
        :param players:
        :return:
        '''
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

        logging.debug("request is called")

        for p in self.room.player_list:
            if p.get_pid() == pid:
                player = p
                break

        self.current_msg_type = msg_type

        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        json_data = json.dumps(message)

        player.send(json_data)
        self.played = player  # set current played player

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

    # TODO: ask dude what's use for this function
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

    # TODO: remove... don't needed to have it
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

    def destroy_room(self):
        '''
        When all round is ended, room is destroyed. Clients get back to robby.
        '''
        # TODO: in current implementation, game result is sended in finish state, so don't have to send result in this function
        # TODO: how to handle error in this function, think about it.
        # TODO: handling about dummy client is needed at later
        # game_log_manager.add_game_log(info1[0], info1[1], info2[0], info2[1], info1[1] == info2[1])
        # game_log_manager.print_all()

        data = {MSG: GAME_HANDLER, MSG_TYPE: GAME_RESULT, DATA: {ERROR_CODE: 0}}

        logging.debug(data)

        json_data = json.dumps(data)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

        for player in self.room.player_list:
            self.players[player.get_pid()] = player
            for attendee in self.observers.values():
                attendee.notice_user_added(player.get_pid())

    def set_delay_time(self, delay_time=0.1):
        self.delay_time = delay_time

    @gen.coroutine
    def delay_action(self):
        yield gen.sleep(self.delay_time)

    # TODO: game result save si realized in here
    def save_game_data(self):
        pass

    # TODO: modification of this function is needed
    # description of this function: when error is caught,
    # this function is called.
    def _exit_handler(self, player):
        pass
