'''
battle.ai

playground is ai battle framework for
1:1:1:1: ... turn game.
'''

import os.path
import sys
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
sys.path.insert(0, '../')
# TODO : find out how to control path and error

from server.handler.playerhandler import PlayerHandler
from server.handler.observerhandler import ObserverHandler
from server.conf.conf_reader import ConfigReader
from server.handler.webpagehandler import *
from server.handler.lobbyhandler import LobbyHandler
from pymongo import MongoClient

class Playground(tornado.web.Application):
    def __init__(self):
        # TODO: game_logic selection must be added, tcp_port, web_port, playing game will be argument of playground.py

        self.player_list = dict()
        self.attendee_list = dict()
        self.lobby_list = dict()

        self.tcp_server = PlayerHandler(self.attendee_list, self.player_list)
        self.db = pymongo.MongoClient()

        self.handler = [

            # websocket handler
            (r"/websocket", ObserverHandler, dict(player_list=self.player_list, attendee_list=self.attendee_list, database=self.db)),
            (r"/lobby/socket", LobbyHandler, dict(player_list=self.player_list, lobby_list=self.lobby_list)),

            # web page handler
            (r"/", IndexHandler),
            (r"/login", LoginPageHandler),
            (r"/lobby", LobbyPageHandler),
            (r"/mypage", MyPageHandler),
            (r"/game", GamePageHandler),

            # signup signin logout request
            (r"/auth/signin", SignInHandler),
            (r"/auth/signup", SignUpHandler),
            (r"/auth/logout", LogoutHandler),
        ]
        self.setting = dict(
            title=u"Battle.ai",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # will be xsrf_cookies=True...... soon
            cookie_secret="123",
            login_url="/auth/login",
            debug=True,
        )
        super(Playground, self).__init__(self.handler, **self.setting)
        self.db = MongoClient()["battle"]

    def may_create_tables(self):
        pass


def main():

    config = ConfigReader()
    config_value = config.read()

    tcp_port = config_value["tcp_port"]
    web_port = config_value["web_port"]

    tornado.options.parse_command_line()
    tornado.options.parse_config_file("my.conf")
    app = Playground()

    io_loop = tornado.ioloop.IOLoop.current()
    app.tcp_server.listen(tcp_port)
    app.listen(web_port)

    print("******************* Battle.AI operate *******************")
    print("                     ...... Created By GreedyOsori ......\n")
    print("Version 0.0")
    io_loop.start()

if __name__ == "__main__":
    main()

