# -*- coding: utf-8 -*-
import functools
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.tcpserver
import tornado.web
import tornado.websocket
from tornado import gen

from server.string import *
from server.gameobject.user import Player
from server.gameobject.message import Message
from server.pools.user_pool import UserPool


class PlayerHandler(tornado.tcpserver.TCPServer):
    def __init__(self):
        tornado.tcpserver.TCPServer.__init__(self)
        # super().__init__(self)

    def handle_stream(self, stream, address):
        """
        when ai client connect to server this function is run
        and spawn_callback (__accept handler)
        :param stream: ai client's stream
        :param address:  ai client's ip address
        """
        tornado.ioloop.IOLoop.current().spawn_callback(self.__accept_handler, stream)

    @gen.coroutine
    def __accept_handler(self, stream):
        '''
        this function accept user_id
        receive protocol is
            msg = {"msg" : "user_info", "msg_type" : "init", "data" : {"username" : userid }}
        if user_id is valid - return y
        else - return n

        :param stream:  player's stream
        '''
        player_pool = UserPool.instance().get_player_pool()
        observer_pool = UserPool.instance().get_observer_pool()

        player = Player(None, stream)
        try:
            while True:
                data = yield player.read()
                message = Message.load_message(data)

                user_key = message.data["username"]

                if user_key in player_pool:
                    data = Message.dump_message(Message(USER_INFO, INIT, {RESPONSE: NO}))
                    stream.write(data.encode())
                    continue
                else:
                    break

            player = Player(user_key, stream)
            data = Message.dump_message(Message(USER_INFO, INIT, {RESPONSE: OK}))
            player.send(data)
            logging.info(user_key + " enter BATTLE.AI")

            # add player in player pool
            player_pool.add_player(player)

            # notify addition of player to observers
            message = Message(USER, ADD, user_key)
            message = Message.dump_message(message)

            lobby_user_pool = UserPool.instance().get_lobby_pool()
            for lobby_user in lobby_user_pool:
                lobby_user.send(message)

            for observer in observer_pool:
                observer.notice_user_added(user_key)

            # register callback for connection close
            # TODO: lambda vs functools.partial
            on_close_func = functools.partial(self._on_close, player)
            stream.set_close_callback(on_close_func)
        except Exception:
            data = Message.dump_message(Message(USER_INFO, INIT, {RESPONSE: NO}))
            stream.write(data.encode())

    def _on_close(self, player):
        '''
        when stream is closed this funciton is run
        :param username: ai client user name
        '''
        logging.info(str(player._id)+" out from BATTLE.AI")

        player_pool = UserPool.instance().get_player_pool()
        observer_pool = UserPool.instance().get_observer_pool()

        player_pool.remove_player(player)

        for observer in observer_pool:
            observer.notice_user_removed(player._id)
