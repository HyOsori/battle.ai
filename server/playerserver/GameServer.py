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
        self.byo_yomi = byo_yomi()
        # end code [0-normal end, 1-abnormal end]

    @gen.coroutine
    def game_handler(self):
        turns = self._select_turns(self.room.player_list)
        print turns
        for turn in turns:
            self.game_logic.onStart(turn)
            print "START"
            for player in self.room.player_list:
                self.q.put(player)
                self._player_handler(player)
            yield self.q.join()
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
        print "send to : "+ player.get_pid()
        print json_data

        player.send(json_data)
        self.byo_yomi.start_timer()

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


class byo_yomi:
    def __init__(self, base_time = 0, turn_time = 30, turn_num = 1):
        self.base_time = base_time
        self.turn_time = turn_time
        self.turn_num = turn_num

    def start_timer(self):
        if self.base_time > 0:
            self.start_time = time.clock()  ## time.clock() is affected by time.sleep()
        elif self.base_time == 0:
            self.count_time(self.turn_time)

    def stop_timer(self):

        pass

    def timeout(self):

        pass

    def count_time(self, time_limit):

        self.current_time = time.clock()

        if self.start_time - self.current_time >  time_limit :
            self.timeout()

