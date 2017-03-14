#-*- coding:utf-8 -*-
import json
import tornado.iostream

from server.string import *
from tornado import gen
from server.handler.gamehandler import GameHandler
from game.omok.OmokGameLogic import OMOKGameLogic
from game.alkaki.AlkakiGameLogic import ALKAKIGameLogic

import server.debugger as logging


class TurnGameHandler(GameHandler):
    def __init__(self, room, players, observers, game_speed, game_logic = None, database = None):
        game_logic = ALKAKIGameLogic(self)
        super(TurnGameHandler, self).__init__(room, players, observers, game_logic)

    @gen.coroutine
    def _play_handler(self):
        logging.debug("play handler is called")
        try:
            self.game_logic.on_ready(self.pid_list)
            logging.debug("on ready is done")
            yield self.request_ready()
            logging.debug("request for ready is done")

            self.game_logic.on_start()
            logging.debug("on start is done")
            while not self.game_end:
                message = yield self.played.timeout_read()
                yield self.delay_action()
                logging.debug("received data: " + str(message))
                message = json.loads(message)
                # TODO: message type check is in dude's code (callback function)
                if message[MSG_TYPE] == self.current_msg_type:
                    # correct message is come
                    self.game_logic.on_action(self.played.get_pid(), message[DATA])
                else:
                    self.handle_game_end(MESSAGE_TYPE_ERROR, {})
        except TimeoutError:
            self.handle_game_end(TIME_OUT, {})
        except json.JSONDecodeError:
            self.handle_game_end(NOT_JSON_DATA, {})
        except tornado.iostream.StreamClosedError:
            self.handle_game_end(CONNECTION_LOST, {})
        except Exception as e:
            logging.error(type(e))
            self.handle_game_end(UNEXPECTED_ERROR, {})

    def request(self, pid, msg_type, data):
        """
        callback function
        game logic call this function to request player's response
        :param pid: player id
        :param msg_type: message type
        :param data: message data
        """

        for p in self.room.player_list:
            if p.get_pid() == pid:
                player = p
                break

        self.current_msg_type = msg_type

        message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        json_data = json.dumps(message)

        player.send(json_data)
        self.played = player  # set current played player

