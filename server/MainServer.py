import tornado.ioloop
import os.path
import sys
sys.path.insert(0,'../')
# TODO : find out how to control path and error

from playerserver.PlayerServer import PlayerServer
from webserver.WebServer import WebServer
from webserver.WebServer import WebSocketServer

TCP_PORT = 9001
WEB_PORT = 9000

class MainServer:
    def __init__(self):
        self.battle_ai_list = dict()
        self.web_client_list = dict()

        self.tcp_server = PlayerServer(self.web_client_list, self.battle_ai_list)

        self.app = tornado.web.Application(
            [
                (r"/websocket", WebSocketServer, dict(battle_ai_list=self.battle_ai_list, web_client_list=self.web_client_list, player_server=self.tcp_server)),
                (r"/", WebServer),
            ],
            template_path=os.path.join(os.path.dirname(__file__), "../templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../static"),
        )

    def run(self):
        io_loop = tornado.ioloop.IOLoop.current()
        self.tcp_server.listen(TCP_PORT)
        self.app.listen(WEB_PORT)

        print("IO LOOP START !!")
        io_loop.start()

if __name__ == "__main__":
    main_server = MainServer()
    main_server.run()
