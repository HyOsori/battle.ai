import tornado.ioloop
import tornado.websocket
import tornado.web
from server.User import Attendee

from server.Room import Room
from server.playerserver.GameServer import GameServer
import json
from server.m_format import *


class WebServer(tornado.web.RequestHandler):
    def get(self):
        self.render("sample.html")

class WebSocketServer(tornado.websocket.WebSocketHandler):

    def initialize(self, web_client_list=dict(), battle_ai_list=dict(), player_server=None):
        self.web_client_list = web_client_list  # dict() - key : conn
        self.battle_ai_list = battle_ai_list  # dict() - key : user_id
        self.player_server = player_server  # PlayerServer

    # accept web_client
    def open(self, *args, **kwargs):
        # make attendee
        new_attendee = Attendee(self)
        self.web_client_list.add(new_attendee)

    def on_message(self, message):

        request = json.loads(message)

        try:
            msg = request[MSG]
            if msg == REQUEST+MATCH:
                self.__response_match(msg[USERS])
                pass
            elif msg == REQUEST+USER_LIST:
                self.__response_user_list()
                pass
            else:
                pass
        except KeyError as e:
            print(e)
            print("WRONG MESSAGE")

    def __response_user_list(self):
        # battle_ai_list's key is user id
        players = self.battle_ai_list.keys()
        msg = {MSG: RESPONSE+USER_LIST, USERS: players}
        json_msg = json.dumps(msg)
        self.write(json_msg)
        pass

    def __response_match(self, pid_list):
        # be care for concurrent access
        players = [self.battle_ai_list[pid] for pid in pid_list]

        room = Room(players, self)
        game_server = GameServer(room)

        tornado.ioloop.IOLoop.spawn_callback(game_server.__game_handler)
        msg = {MSG: RESPONSE+MATCH, ERROR: 0, USERS: pid_list}
        json_msg = json.dumps(msg)
        self.write(json_msg)

    def on_close(self):
        pass

