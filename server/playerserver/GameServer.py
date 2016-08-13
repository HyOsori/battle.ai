#-*- coding:utf-8 -*-
from tornado import queues, gen
import json
import time
from server.m_format import *

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

        self.time_delay = 0.5

        self.game_result = {}
        self.error_msg = "none"

        self.current_msg_type = -1
        self.error_code = 1
        # end code [0-normal end, 1-abnormal end]

    @gen.coroutine
    def game_handler(self):
        try:
            turns = self._select_turns(self.room.player_list)
            print turns
            for turn in turns:
                self.game_logic.onStart(turn)
                print "START"
                for player in self.room.player_list:
                    self.q.put(player)
                    self._player_handler(player)
                yield self.q.join()
        except Exception as e:
            print "[!]ERROR : "+e
            self.game_logic.onError('test')
        finally:
            print "END"
            self.destroy_room()

    def _select_turns(self, players):
        turn = [player.get_pid() for player in players]
        return [turn, turn]

    def _player_handler(self, player):
        raise NotImplementedError

    def request(self, pid, msg_type, game_data):
        for p in self.room.player_list:
            if p.get_pid() == pid:
                player = p
        self.current_msg_type = msg_type

        data = {MSG: GAME_DATA, MSG_TYPE: msg_type, GAME_DATA: game_data}
        json_data = json.dumps(data)
        print "send to : "+player.get_pid()
        print json_data

        player.send(json_data)

    def notify(self, msg, game_data):
        data = {MSG: GAME_DATA, MSG_TYPE: msg, GAME_DATA: game_data}
        json_data = json.dumps(data)

        for player in self.room.player_list:
            player.send(json_data)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

    def onEnd(self, is_valid_end, game_data, error_msg="none"):
        self.game_result = game_data
        self.error_msg = error_msg

        if is_valid_end:
            self.error_code = 0
            data = {MSG: GAME_DATA, MSG_TYPE: ROUND_RESULT, GAME_DATA: game_data}
        else:
            self.error_code = 1
            data = {MSG: GAME_RESULT, ERROR: self.error_code, ERROR_MSG: error_msg, GAME_DATA: game_data}

        json_data = json.dumps(data)

        for player in self.room.player_list:
            player.send(json_data)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)

    def destroy_room(self):

        data = {MSG: GAME_RESULT, ERROR: self.error_code, ERROR_MSG: self.error_msg, GAME_DATA: self.game_result}

        json_data = json.dumps(data)
        for attendee in self.room.attendee_list:
            attendee.send(json_data)

        for player in self.room.player_list:
            self.battle_ai_list[player.get_pid()] = player
            for attendee in self.web_client_list.values():
                attendee.notice_user_added(player.get_pid())

    def set_delay_time(self, delay_time=0.5):
        self.time_delay = delay_time

    def delay_action(self):
        time.sleep(self.time_delay)

    def save_game_data(self):
        pass
