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
        self.delay_time = self.time_delay_list[time_index]

        self.init_data_dict = {}

        self.current_msg_type = "start"  # TODO: remove
        self.game_end = False

        self.game_end = False

        self.played = None  # player currently finished turn

    @gen.coroutine
    def run(self):
        """
        Handle game playing
        """
        logging.info("=====Game Start=====")
        yield self._play_handler(None)
        logging.info("=====Game End=====")
        self.destroy_room()
        logging.info("=====Destroy Room=====")

    def _play_handler(self):
        '''
        handle player's game playing
        :param player: player object
        '''
        raise NotImplementedError

    @gen.coroutine
    def request_ready(self):
        try:
            for pid, init_data in self.init_data_dict:
                player = self.find_player_by_pid(pid)
                player.send(json.dumps(init_data))

                message = yield player.read()
                message = json.loads(message)

                if message[MSG_TYPE] == READY and message[MSG_TYPE][RESPONSE] == OK:
                    pass
                else:
                    # set error code for game end
                    return False
        except Exception as e:
            e.with_traceback(None)
            return False

    def on_init_game(self, init_data_dict):
        self.init_data_dict = init_data_dict

    def find_player_by_pid(self, pid):
        for player in self.room.player_list:
            if pid == player.pid:
                return player
        return None

    def request(self, pid, msg_type, data):
        """
        callback function
        game logic call this function to request player's response
        :param pid: player id
        :param msg_type: message type
        :param data: message data
        """
        raise NotImplementedError

    def notify(self, msg_type, data):
        """
        callback function
        game logic call this function to notify game data
        :param msg_type: notifying message
        :param data: message data
        """
        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        json_data = json.dumps(message)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

    def on_end(self, error_code, message):
        """
        callback function
        when game is ended this function is called by GameLogic
        :param is_valid_end: 0 (normal end), 1 (abnormal end)
        :param message: game result information
        """
        self.handle_game_end(error_code, message)

    def handle_game_end(self, error_code, message={}):
        message = {MSG: GAME_HANDLER, MSG_TYPE: END, ERROR_CODE: error_code, DATA: message}
        message = json.dumps(message)

        for player in self.room.player_list:
            player.send(message)
        for attendee in self.room.attendee_list:
            attendee.send(message)

        self.game_end = True

    def destroy_room(self):
        """
        When all round is ended, room is destroyed. Clients get back to robby.
        """

        # TODO: player add and remove ... how to deal with it? remove from list or set flag on player
        # TODO: => set flag is better .
        for player in self.room.player_list:
            self.players[player.get_pid()] = player
            for attendee in self.observers.values():
                attendee.notice_user_added(player.get_pid())

    @gen.coroutine
    def delay_action(self):
        yield gen.sleep(self.delay_time)
