#-*- coding:utf-8 -*-
from tornado import queues, gen
import json
from server.m_format import *

import server.ServerLog as logging

"""
GameServer (for all games, abstract class)

TurnGameServer (for turn games)
RealTimeGameServer (for real time games, not yet)
"""


class GameServer:
    def __init__(self, room, player_list, attendee_list, game_logic,  time_index=4, database=None):
        self.game_logic = game_logic
        self.room = room
        self.player_list = player_list  # WHY NEEDED? - when game room destroy - player added in list
        self.attendee_list = attendee_list  # WHY NEEDED? - when game room destroy - attendee.notify_user_added
        self.q = None

        self.time_delay_list = [2, 0.5, 0.3, 0.1, 0.05]

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

        self.q = queues.Queue(len(self.room.player_list))

        for turn in self.turns:
            # check game normal flag
            if not self.normal_game_playing:
                break

            logging.info("=====Are You Ready=====")
            ready = yield self.__ready_check(self.room.player_list)
            logging.debug("ready status : " + str(ready))
            if not ready:
                return

            logging.info("==================Game Start==================")
            self.game_logic.on_start(turn)

            logging.debug("normal game playinng ........")

            for player in self.room.player_list:
                self.q.put(player)
                self._player_handler(player)
            yield self.q.join()
            logging.info("==============Game End=============")
        self.destroy_room()
        logging.info("==========Destroy Room==========")

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
        msg = {MSG: GAME_HANDLER, MSG_TYPE: READY, DATA: {}}
        cur_player = None
        try:
            data = json.dumps(msg)
            for player in players:
                cur_player = player
                player.send(data)
                recv_data = yield player.read()
                recv_msg = json.loads(recv_data)
                logging.debug(recv_msg)
                if not recv_msg[DATA][RESPONSE] == 'OK':
                    return_flag = False
                    raise gen.Return(False)
            # recv Are you ready message

            # send web that all player ready OK
            recv_msg[DATA] = {RESPONSE_: OK, PLAYERS: [player.get_pid() for player in players]}
            data = json.dumps(recv_msg)
            for attendee in self.room.attendee_list:
                attendee.send(data)
            logging.debug("return True")
            return_flag = True
            raise gen.Return(True)
        except Exception as e:
            if return_flag:
                raise gen.Return(True)
            for p in self.room.player_list:
                if not p.get_pid() == cur_player.get_pid():
                    self.player_list[p.get_pid()] = p
            logging.error(e)
            logging.error("ready error")
            raise gen.Return(False)

    def _error_handler(self):
        pass

    def _player_handler(self, player):
        '''
        handle player's game playing
        :param player: player object
        '''
        raise NotImplementedError

    def request(self, pid, msg_type, data):
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

        logging.error("cur msg_type :"+msg_type + "  changed msg_type :" + self.current_msg_type)
        self.current_msg_type = msg_type

        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        json_data = json.dumps(message)

        logging.info("request to "+player.get_pid())
        logging.info(json_data)

        player.send(json_data)

    def notify(self, msg_type, data):
        '''
        callback function
        game logic call this function to notify game data
        :param msg_type: notifying message
        :param data: message data
        '''
        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        json_data = json.dumps(message)

        logging.info(json_data)

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
        logging.info("on_end() function is called")

        self.game_result = message

        if is_valid_end:
            self.game_end = True
            message = {MSG: GAME_DATA, MSG_TYPE: ROUND_RESULT, DATA: message}
            self.round_result = message
        else:
            logging.error("logic error end")
            raise Exception

        json_data = json.dumps(message)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

    def send_round_result(self, round_result):
        # save round result, temporary implementation ..;;
        try:
            score_sum = [0, 0]

            score_data = round_result[DATA]["score"]
            score_sum[0] = score_data[0][0] + score_data[1][0]
            score_sum[1] = score_data[1][0] + score_data[1][1]

            if score_sum[0] > score_sum[1]:
                self.score[0] += 1
            elif score_sum[0] < score_sum[1]:
                self.score[1] += 1

            logging.error("cur msg_type :" + self.current_msg_type + "  changed msg_type :" + ROUND_RESULT)
            self.current_msg_type = ROUND_RESULT
            json_data = json.dumps(round_result)
        except Exception as e:
            logging.error(round_result)
            json_data = "error"

        logging.debug("Send Round Result : " + json_data)
        for player in self.room.player_list:
            player.send(json_data)

    def destroy_room(self):
        '''
        When all round is ended, room is destroyed. Clients get back to robby.
        '''
        # TODO: game_result must chagned to real game_result, not round result

        # make game result, temporary implementation.. ;;
        result = []
        try:
            info1 = [self.room.player_list[0].get_pid(), self.score[0]]
            info2 = [self.room.player_list[1].get_pid(), self.score[1]]
            result.append(info1)
            result.append(info2)
        except Exception as e:
            logging.error(e)

        # game_log_manager.add_game_log(info1[0], info1[1], info2[0], info2[1], info1[1] == info2[1])
        # game_log_manager.print_all()

        data = {MSG: GAME_HANDLER, MSG_TYPE: GAME_RESULT, DATA: result}

        logging.debug(data)

        json_data = json.dumps(data)
        for attendee in self.room.attendee_list:
            attendee.send(json_data)

        logging.info(str(self.room.player_list))
        logging.info("-----------------Destory room----------------------------")

        for player in self.room.player_list:
            self.player_list[player.get_pid()] = player
            for attendee in self.attendee_list.values():
                attendee.notice_user_added(player.get_pid())

    def set_delay_time(self, delay_time=0.1):
        self.delay_time = delay_time

    @gen.coroutine
    def delay_action(self):
        yield gen.sleep(self.delay_time)

    def save_game_data(self):
        pass

    def _exit_handler(self, player):
        logging.error("exit error handler")
        self.game_logic.on_error(player.get_pid())
        self.normal_game_playing = False
        for p in self.room.player_list:
            if p.get_pid() == player.get_pid():
                self.room.player_list.remove(p)
            self.q.get()
            self.q.task_done()
        gen.Return(None)



