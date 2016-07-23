import tornado.ioloop

from server.webserver.WebServer import WebServer


class MainServer:
    def __init__(self):
        self.battle_ai_list = dict()
        self.web_client_list = set()

        # self.tcp_server = TurnGameServer(self.battle_ai_list, self.web_client_list)
        self.app = tornado.web.Application([
            (r"/", WebServer, dict(battle_ai_list=self.battle_ai_list, web_client_list=self.web_client_list, player_server=self.tcp_server)),
        ])

    def run(self):
        io_loop = tornado.ioloop.IOLoop.current()

        self.tcp_server.listen(8000)
        self.app.listen(8800)

        print "IO LOOP START !!"
        io_loop.start()

if __name__ == "__main__":
    main_server = MainServer()
    main_server.run()



