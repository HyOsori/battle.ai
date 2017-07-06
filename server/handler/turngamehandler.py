#-*- coding:utf-8 -*-
import json
import tornado.iostream

from server.string import *
from tornado import gen
from server.handler.gamehandler import GameHandler
from server.gameobject.message import Message
from game.omok.OmokGameLogic import OMOKGameLogic
import traceback
from game.alkaki.alkaki_gamelogic import ALKAKIGameLogic

import server.debugger as logging


class TurnGameHandler(GameHandler):
    def __init__(self, room):
        game = OMOKGameLogic(self)
        super().__init__(room, game)

    @gen.coroutine
    def _play_handler(self):
        logging.info("play handler is called")
        try:
            self.game.on_ready(self._ids)
            logging.info("on ready is done")
            yield self.request_ready()
            logging.info("request for ready is done")

            self.game.on_start()
            logging.info("on start is done")
            while not self.game_end:
                message = yield self.played.timeout_read()
                yield self.delay_action()
                logging.info("received data: " + str(message))
                message = Message.load_message(message)
                # TODO: message type check is in dude's code (callback function)
                if message.msg_type == self.current_msg_type:
                    # correct message is come
                    self.game.on_action(self.played._id, message.data)
                else:
                    self.handle_game_end(MESSAGE_TYPE_ERROR, {})
        except TimeoutError:
            self.handle_game_end(TIME_OUT, {})
        except json.JSONDecodeError:
            self.handle_game_end(NOT_JSON_DATA, {})
        except tornado.iostream.StreamClosedError:
            self.handle_game_end(CONNECTION_LOST, {})
        except Exception as e:
            traceback.print_tb(e)
            logging.error("unexpected exception: " + str(repr(e)) + "  " + str(type(e)))
            self.handle_game_end(UNEXPECTED_ERROR, {})

    def request(self, _id, msg_type, data):
        logging.info("request is called")
        """
        callback function
        game logic call this function to request player's response
        :param pid: player id
        :param msg_type: message type
        :param data: message data
        """

        for player in self.room.player_list:
            if player._id == _id:
                selected_player = player
                break

        self.current_msg_type = msg_type

        data = Message.dump_message(Message(GAME_DATA, msg_type, data))
        player.send(data)

        self.played = player  # set current played player
