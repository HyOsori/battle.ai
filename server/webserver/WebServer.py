import tornado.ioloop
import tornado.websocket
import tornado.web
from server.User import Attendee

from server.Room import Room
from server.playerserver.TurnGameServer import TurnGameServer
import json
from server.m_format import *

import logging


class WebServer(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class LogHandler(tornado.web.RequestHandler):
    def initialize(self, database_driver):
        self.db = database_driver

    def get(self):
        name = self.get_argument('name', None)
        length = self.get_argument('length', default=10)
        searched = ''

        if name:
            searched = self.db.search_game_log(cnt=length)
        else:
			searched = self.db.search_game_log(name=name, cnt=length)
        self.write(json.dumps(searched))

    def put(self): #log update
        winner = self.get_argument('winner')
        win_score = self.get_argument('win_score')
        loser = self.get_argument('loser')
        lose_score = self.get_argument('lose_score')
        self.db.add_game_log(winner, win_score, loser, lose_score)
        self.write('OK')



class WebSocketServer(tornado.websocket.WebSocketHandler):

    def initialize(self, attendee_list=dict(), player_list=dict(), player_server=None, database=None):
        '''

        :param attendee_list:
        :param player_list:
        :param player_server:
        '''
        self.attendee_list = attendee_list  # dict() - key : conn
        self.player_list = player_list  # dict() - key : user_id
        self.player_server = player_server  # PlayerServer
        self.database = database

    def open(self, *args, **kwargs):
        '''
        open websocket
        '''
        new_attendee = Attendee(self)
        self.attendee_list[self] = new_attendee

    def on_message(self, message):
        '''
        When receive message from Attendee, this function runs.
        :param message: message from Attendee
        '''
        logging.debug(message)
        request = json.loads(message)
        try:
            msg = request[MSG]
            if msg == REQUEST+MATCH:
                self._response_match(request[DATA])
            elif msg == REQUEST+USER_LIST:
                self._response_user_list()
            else:
                pass
        except Exception as e:
            logging.error(str(e) + "// wrong message")

    def _response_user_list(self):
        self.attendee_list[self].attendee_flag = False

        players = list(self.player_list.keys())

        msg = {MSG: RESPONSE_ + USER_LIST, USERS: players}
        json_msg = json.dumps(msg)

        try:
            self.write_message(json_msg)
        except Exception as e:
            logging.error(e)
            self.attendee_list.pop(self)

    def _response_match(self, data):
        try:
            players = [self.player_list.pop(pid) for pid in data[USERS]]
            logging.error(type(data[USERS][0]))
        except Exception as e:
            logging.error(e)
            return

        for pid in data[USERS]:
            for attendee in self.attendee_list.values():
                attendee.notice_user_removed(pid)
        try:
            room = Room(players, self.attendee_list[self])
            game_server = TurnGameServer(room, self.player_list, self.attendee_list, int(data[SPEED]))
        except Exception as e:
            logging.error(e)
            logging.error("During making room, error is occured")
            return

        tornado.ioloop.IOLoop.current().spawn_callback(game_server.game_handler)
        speed_list = [2, 0.5, 0.3, 0.1, 0.05]
        msg = {MSG: RESPONSE_ + MATCH, DATA: {USERS: data[USERS], ERROR: 0, SPEED: speed_list[int(data[SPEED])]}}
        json_msg = json.dumps(msg)

        try:
            self.write_message(json_msg)
            self.attendee_list[self].room_enter()
        except Exception as e:
            logging.error(e)
            self.attendee_list.pop(self)

    # TODO : find out how to deal with this error (CORS)
    def check_origin(self, origin):
        return True

    def on_close(self):
        self.attendee_list.pop(self)
