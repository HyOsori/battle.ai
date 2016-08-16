# -*- coding: utf-8 -*-

import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.tcpserver

from server.User import Player

from tornado import gen


class PlayerServer(tornado.tcpserver.TCPServer):
    def __init__(self, web_client_list, battle_ai_list):
        tornado.tcpserver.TCPServer.__init__(self)
        self.battle_ai_list = battle_ai_list
        self.web_client_list = web_client_list

    def handle_stream(self, stream, address):
        print("accept client")
        tornado.ioloop.IOLoop.current().spawn_callback(self.__accept_handler__, stream)

    @gen.coroutine
    def __accept_handler__(self, stream):
        recv = yield stream.read_bytes(256, partial=True)
        name = json.loads(recv)
        username = name["username"]
        player = Player(username, stream)
        print(username + " enter the game")

        self.battle_ai_list[username] = player
        for attendee in self.web_client_list.values():
            attendee.notice_user_added(username)
