# -*- coding: utf-8 -*-

import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.tcpserver
import functools

from server.User import Player

from tornado import gen


class PlayerServer(tornado.tcpserver.TCPServer):
    def __init__(self, web_client_list, battle_ai_list):
        tornado.tcpserver.TCPServer.__init__(self)
        self.battle_ai_list = battle_ai_list
        self.web_client_list = web_client_list

    def handle_stream(self, stream, address):
        print("accept client")
        tornado.ioloop.IOLoop.current().spawn_callback(self._accept_handler, stream)

    @gen.coroutine
    def _accept_handler(self, stream):
        recv = yield stream.read_bytes(256, partial=True)
        msg = json.loads(recv)
        """
            msg = {"msg" : "user_info", "msg_type" : "init", "user_data" : {"username" : userid }}
        """
        username = msg["user_data"]["username"]

        if username in self.battle_ai_list.keys():
            # in case that duplicate id is detected
            pass

        player = Player(username, stream)
        print(username + " enter the game")

        self.battle_ai_list[username] = player
        for attendee in self.web_client_list.values():
            attendee.notice_user_added(username)

        on_close_func = functools.partial(self._on_close, username)
        stream.set_close_callback(on_close_func)


    def _on_close(self, username):
        print 'Socket ' + username + ' Closed'

        try:
            self.battle_ai_list.pop(username)
        except Exception as e:
            print e

        for attendee in self.web_client_list.values():
            attendee.notice_user_removed(username)