import tornado.ioloop
import os.path
import sys
sys.path.insert(0,'../')
# TODO : find out how to control path and error

from playerserver.PlayerServer import PlayerServer
from webserver.WebServer import WebServer
from webserver.WebServer import WebSocketServer, LogHandler
from server.database.MysqlDriver import LogDB

import logging

TCP_PORT = 9001
WEB_PORT = 9000


class MainServer:
    def __init__(self):

        # TODO: game_logic selection must be added, tcp_port, web_port, playing game will be argument of MainServer.py

        self.player_list = dict()
        self.attendee_list = dict()

        self.tcp_server = PlayerServer(self.attendee_list, self.player_list)

        # db = LogDB()
        db = 1
        # db.open()

        self.app = tornado.web.Application(
            [
                (r"/websocket", WebSocketServer, dict(player_list=self.player_list, attendee_list=self.attendee_list, player_server=self.tcp_server)),
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
        io_loop = tornado.ioloop.IOLoop.current()
        self.tcp_server.listen(TCP_PORT)
        self.app.listen(WEB_PORT)

        logging.info("IOLoop is started")
        io_loop.start()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        TCP_PORT = int(sys.argv[1])
        WEB_PORT = int(sys.argv[2])

    main_server = MainServer()
    main_server.run()
