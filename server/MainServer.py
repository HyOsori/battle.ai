import tornado.ioloop
import os.path
import sys
sys.path.insert(0,'../')
# TODO : find out how to control path and error

from playerserver.PlayerServer import PlayerServer
from webserver.WebServer import WebServer
from webserver.WebServer import WebSocketServer, LogHandler
from server.database.MysqlDriver import LogDB
from config_reader import ConfigReader

from server.game_log_manager import GameLogManager

import logging

TCP_PORT = 9001
WEB_PORT = 9000

game_log_manager = GameLogManager()

class MainServer:
    def __init__(self):

        # TODO: game_logic selection must be added, tcp_port, web_port, playing game will be argument of MainServer.py

        self.player_list = dict()
        self.attendee_list = dict()

        self.tcp_server = PlayerServer(self.attendee_list, self.player_list)


        db = None
        # db = LogDB()
        # db.open()

        self.config = ConfigReader()

        self.app = tornado.web.Application(
            [
                (r"/websocket", WebSocketServer, dict(player_list=self.player_list, attendee_list=self.attendee_list, player_server=self.tcp_server, database=db)),
                (r'/log', LogHandler, dict(database_driver=db)),
                (r"/", WebServer),
            ],
            template_path=os.path.join(os.path.dirname(__file__), "../templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../static"),
        )

    def run(self):
        '''
        Start server
        run webserver and tcpserver
        webserver : manage attendee
        tcpserever : manage ai_client
        '''

        config_value = self.config.read()

        tcp_port = config_value["tcp_port"]
        web_port = config_value["web_port"]

        io_loop = tornado.ioloop.IOLoop.current()
        self.tcp_server.listen(tcp_port)
        self.app.listen(web_port)

        logging.info("IOLoop is started")
        io_loop.start()

if __name__ == "__main__":

    main_server = MainServer()
    main_server.run()
