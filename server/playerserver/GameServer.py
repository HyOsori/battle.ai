#-*- coding:utf-8 -*-
from tornado import queues, gen
import json
import time
from server.m_format import *

import server.ServerLog as logging

"""
GameServer (for all games, abstract class)

TurnGameServer (for turn games)
RealTimeGameServer (for real time games, not yet)
"""


class GameServer:
    def __init__(self, room, battle_ai_list, web_client_list, game_logic):
        self.game_logic = game_logic
        self.room = room
        self.battle_ai_list = battle_ai_list
        self.web_client_list = web_client_list
        self.q = queues.Queue()

        self.time_delay = 0.1

        self.game_result = {}
        self.error_msg = "none"

        self.current_msg_type = -1
        self.error_code = 1
        self.turns = []

    @gen.coroutine
    def game_handler(self, round_num = 0):
        '''
        :param
        round_num: number of round to play game
        handle game playing
        '''
        self.turns = self._select_turns(self.room.player_list)

        for turn in self.turns:
            logging.debug("=====Are You Ready=====")
            self.game_logic.on_start(turn)
            logging.debug("==================Game Start==================")
            print "START"
            for player in self.room.player_list:
                self.q.put(player)
                self._player_handler(player)
            yield self.q.join()
            logging.debug("==============Game End=============")
        self.destroy_room()
        logging.debug("==========Destroy Room==========")

    def _select_turns(self, players):
        turn = [player.get_pid() for player in players]

        return [turn, [turn[1], turn[0]]]

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

        self.current_msg_type = msg_type

        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, GAME_DATA: data}
        json_data = json.dumps(message)

        logging.debug("send to "+player.get_pid())
        logging.debug(json_data)

        player.send(json_data)

    def notify(self, msg_type, data):
        '''
        callback function
        game logic call this function to notify game data
        :param msg_type: notifying message
        :param data: message data
        '''
        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, GAME_DATA: data}
        json_data = json.dumps(message)

        logging.debug(json_data)

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
        logging.debug("on_end() function is called")

        self.game_result = message

        if is_valid_end:
            message = {MSG: GAME_DATA, MSG_TYPE: ROUND_RESULT, GAME_DATA: message}
        else:
            # TODO: do not excute this code, - go to destory_room naturally
            message = {MSG: GAME_HANDLER, MSG_TYPE: GAME_RESULT, GAME_DATA: DATA}

            json_data = json.dumps(message)

            for player in self.room.player_list:
                player.send(json_data)

            for attendee in self.room.attendee_list:
                attendee.send(json_data)


            # TODO : memory lack error must be corrected!!

            for x in range(len(self.turns)):
                self.q.get()
            return

        json_data = json.dumps(message)

        for player in self.room.player_list:
            player.send(json_data)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

    def destroy_room(self):
        '''
        When all round is ended, room is destroyed. Clients get back to robby.
        '''
        # TODO: game_result must chagned to real game_result, not round result
        data = {MSG: GAME_RESULT, ERROR: self.error_code, ERROR_MSG: self.error_msg, GAME_DATA: self.game_result}

        json_data = json.dumps(data)
        for attendee in self.room.attendee_list:
            attendee.send(json_data)

        logging.debug(str(self.room.player_list))
        logging.info("-----------------Destory room----------------------------")

        for player in self.room.player_list:
            self.battle_ai_list[player.get_pid()] = player
            for attendee in self.web_client_list.values():
                attendee.notice_user_added(player.get_pid())

    def set_delay_time(self, delay_time=0.1):
        self.time_delay = delay_time

    def delay_action(self):
        time.sleep(self.time_delay)

    def save_game_data(self):
        pass
