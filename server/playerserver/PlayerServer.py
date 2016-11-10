# -*- coding: utf-8 -*-

import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.tcpserver
import functools
from server.m_format import *

from server.User import Player

from tornado import gen

import logging


class PlayerServer(tornado.tcpserver.TCPServer):
    def __init__(self, attendee_list, player_list):
        tornado.tcpserver.TCPServer.__init__(self)
        self.player_list = player_list
        self.attendee_list = attendee_list

    def handle_stream(self, stream, address):
        '''
        when ai client connect to server this function is run
        and spawn_callback (__accept handler)
        :param stream: ai client's stream
        :param address:  ai client's ip address
        '''
        logging.debug("accept client is done")
        tornado.ioloop.IOLoop.current().spawn_callback(self.__accept_handler, stream)

    @gen.coroutine
    def __accept_handler(self, stream):
        '''
        this function accept user_id
        receive protocol is
            msg = {"msg" : "user_info", "msg_type" : "init", "data" : {"username" : userid }}
        if user_id is valid - return y
        else - return n

        :param stream:  ai_client's stream
        '''
        # TODO : set protocol of user_info, and handle exception of every case
        try:
            while True:
                recv = yield stream.read_bytes(128, partial=True)
                logging.debug(recv)
                msg = json.loads(recv)

                username = msg[DATA]["username"]

                # temporary implementation ;;
                if not username == 'Dummy3':
                    logging.error("user name : " + username)
                    logging.error(self.player_list.keys())
                    if username in self.player_list.keys():
                        logging.error("ID Already exists!!")
                        msg = {MSG: USER_INFO, MSG_TYPE:INIT, DATA: {RESPONSE: NO}}
                        json_data = json.dumps(msg)
                        stream.write(json_data)
                        continue
                        # logging.info(str(unicode(username)))
                        # username = str(unicode(username))
                    break
                else:
                    print "dummy add"
                    break

            player = Player(username, stream)
            print(username + " enter the game")

            self.player_list[username] = player
            for attendee in self.attendee_list.values():
                attendee.notice_user_added(username)

            on_close_func = functools.partial(self._on_close, username)
            stream.set_close_callback(on_close_func)
        except Exception as e:
            logging.error(e)
            msg = {MSG: USER_INFO, MSG_TYPE: INIT, DATA: {RESPONSE: NO}}
            json_data = json.dumps(msg)
            stream.write(json_data)

    def _on_close(self, username):
        '''
        when stream is closed this funciton is run
        :param username: ai client user name
        '''

        logging.debug(str(username)+"'s stream is closed")

        try:
            self.player_list.pop(username)
        except Exception as e:
            logging.debug("In player stream closed, pop error")

        for attendee in self.attendee_list.values():
            attendee.notice_user_removed(username)
