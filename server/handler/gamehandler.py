# -*- coding:utf-8 -*-
from tornado import queues, gen
import json
from server.string import *
from server.gameobject.message import Message
from server.pools.user_pool import UserPool
from server.db.dbhelper import DBHelper
from server.model.gamelog import GameLog

import server.debugger as logging


"""
GameServer (for all games, abstract class)

"""


class GameHandler:
    def __init__(self, room, game):
        self.game = game
        self.room = room  # player objects and observer objects are in here
        self._ids = [player._id for player in self.room.player_list]

        self.delay_time = 0

        self.init_data_dict = {}

        self.current_msg_type = "start"  # TODO: remove
        self.game_end = False
        self.played = None  # player currently finished turn

        self.game_message_list = []

        self.game_result = ""

    @gen.coroutine
    def run(self):
        """
        Handle game playing
        """
        logging.info("=====Game Start=====")
        yield self._play_handler()
        logging.info("=====Game End=====")
        self.destroy_room()

    def _play_handler(self):
        '''
        handle player's game playing
        :param player: player object
        '''
        raise NotImplementedError

    @gen.coroutine
    def request_ready(self):

        # notify initial data to observers
        for observer in self.room.observer_list:
            data = Message.dump_message(Message(GAME_HANDLER, READY, self.init_data_dict))
            observer.send(data)

        # send initial data to players
        for _id, init_data in self.init_data_dict.items():
            player = self.find_player(_id)
            data = Message.dump_message(Message(GAME_HANDLER, READY, init_data))
            player.send(data)

            message = yield player.read()
            message = Message.load_message(message)

            # and check response is OK or not
            if message.msg_type == READY and message.data[RESPONSE] == OK:
                pass
            else:
                # set error code for game end
                return False

    def on_init_game(self, init_data_dict):
        """
        callback function used at game part
        game part set init_data_dict using this function.

        :param init_data_dict:
        """
        self.init_data_dict = init_data_dict

    def find_player(self, _id):
        for player in self.room.player_list:
            if _id == player._id:
                return player
        return None

    def request(self, _id, msg_type, data):
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

        data = Message.dump_message(Message(GAME_DATA, msg_type, data))

        # data to save in database
        self.game_message_list.append(data)

        for observer in self.room.observer_list:
            observer.send(data)

    def on_end(self, error_code, message):
        """
        callback function
        when game is ended this function is called by GameLogic
        :param is_valid_end: 0 (normal end), 1 (abnormal end)
        :param message: game result information
        """
        self.handle_game_end(error_code, message)

    def handle_game_end(self, error_code, message={}):

        self.game_result = message
        data = Message.dump_message(Message(GAME_HANDLER, END, message, error_code))

        for player in self.room.player_list:
            player.send(data)
        for observer in self.room.observer_list:
            observer.send(data)

        self.game_end = True

    def destroy_room(self):
        """
        When all round is ended, room is destroyed. Clients get back to robby.
        """
        logging.info("=====Destroy Room=====")

        game_log = GameLog()
        game_log.players = self._ids
        game_log.game_result = self.game_result
        game_log.game_message_list = self.game_message_list

        db = DBHelper.instance().db
        db.game_log_list.insert(game_log.__dict__)

        observer_pool = UserPool.instance().get_observer_pool()

        for player in self.room.player_list:
            player.room_out()
            for observer in observer_pool:
                observer.notice_user_added(player._id)

    @gen.coroutine
    def delay_action(self):
        yield gen.sleep(self.delay_time)
