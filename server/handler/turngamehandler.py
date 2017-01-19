#-*- coding:utf-8 -*-
import json

from server.string import *
from tornado import gen
from server.handler.gamehandler import GameHandler
from game.pixels.PixelsGameLogic import PixelsGameLogic

import server.debugger as logging


class TurnGameHandler(GameHandler):
    def __init__(self, room, players, observers, game_speed, game_logic = None, database = None):
        game_logic = PixelsGameLogic(self)
        super(TurnGameHandler, self).__init__(room, players, observers, game_logic)

        # temporary implemenation
        self.message_end = False

    @gen.coroutine
    def _play_handler(self, player):
        logging.debug("play handler is called")
        try:
            self.game_logic.on_start(self.pid_list)
            logging.debug("on start is done")
            while True:
                logging.debug("looping ...")
                message = yield self.received_data
                logging.debug("received data: " + str(message))
                message = json.loads(message.decode())
                # TODO: message type check is in dude's code (callback function)
                if message[MSG_TYPE] == self.current_msg_type:
                    # temporary implementation ;; must be del
                    # TODO: game_result + round_result = result ...
                    if message[MSG_TYPE] == GAME_RESULT:
                        logging.error("game result receive!!!!!!")
                        break

                    if message[MSG_TYPE] == "finish":
                        if not self.message_end:
                            self.message_end = True
                        else:
                            break


                    # correct message is come
                    self.game_logic.on_action(self.played.get_pid(), message[DATA])
                    # if res[MSG_TYPE] == FINISH:
                    #     if self.game_end:
                    #         self.send_round_result(self.round_result)
                else:
                    # TODO: error case classification
                    logging.debug("error case1")
                    pass
        except Exception as e:
            # TODO: error case classification
            logging.debug(e.with_traceback())
            logging.debug("error case2")
            pass
