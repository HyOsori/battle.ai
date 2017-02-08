#-*- coding:utf-8 -*-
import json

from server.string import *
from tornado import gen
from server.handler.gamehandler import GameHandler
from game.omok.OmokGameLogic import OmokGameLogic

import server.debugger as logging


class TurnGameHandler(GameHandler):
    def __init__(self, room, players, observers, game_speed, game_logic = None, database = None):
        game_logic = OmokGameLogic(self)
        super(TurnGameHandler, self).__init__(room, players, observers, game_logic)

        # temporary implementation
        self.message_end = False

    @gen.coroutine
    def _play_handler(self, player):
        logging.debug("play handler is called")
        try:
            self.game_logic.on_start(self.pid_list)
            logging.debug("on start is done")
            while True:
                message = yield self.played.read()
                logging.debug("received data: " + str(message))
                message = json.loads(message.decode())
                # TODO: message type check is in dude's code (callback function)
                if message[MSG_TYPE] == self.current_msg_type:

                    if message[MSG_TYPE] == FINISH:
                        self.pid_list.remove(self.played.get_pid())
                        if len(self.pid_list) == 0:
                            break

                    # correct message is come
                    self.game_logic.on_action(self.played.get_pid(), message[DATA])
                else:
                    # TODO: error case classification
                    logging.debug("error case1")
                    pass
        except Exception as e:
            # TODO: error case classification
            logging.debug(e.with_traceback())
            logging.debug("error case2")
            pass
