# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.tcpserver
from server.User import User

from tornado import gen


class PlayerServer(tornado.tcpserver.TCPServer):
    def __init__(self, web_client_list, battle_ai_list):
        tornado.tcpserver.TCPServer.__init__(self)
        self.battle_ai_list = battle_ai_list
        self.web_client_list = web_client_list

    def handle_stream(self, stream, address):
        tornado.ioloop.IOLoop.current().spawn_callback(self.__accept_handler__, stream)

    @gen.coroutine
    def __accept_handler__(self, stream):
        pid = stream.read_bytes(256, partial=True)
        player = User.Player(pid, stream)

        self.battle_ai_list.append(player)
        for attendee in self.web_client_list:
            attendee.notice_user_added(pid)
