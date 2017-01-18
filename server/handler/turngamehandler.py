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

    @gen.coroutine
    def _play_handler(self, player):
        try:
            self.game_logic.on_start(self.pid_list)
            logging.debug("on_start is done")
            while True:
                yield self.delay_action()
                # TODO: message type check is in dude's code (callback function)
                if self.received_data[MSG_TYPE] == self.current_msg_type:
                    # temporary implementation ;; must be del
                    # TODO: game_result + round_result = result ...
                    if self.received_data[MSG_TYPE] == GAME_RESULT:
                        logging.error("game result receive!!!!!!")
                        break

                    if self.received_data[MSG_TYPE] == ROUND_RESULT:
                        logging.error("roudn result reciv")
                        self.q.get()
                        self.q.task_done()
                        break

                    # correct message is come
                    yield self.game_logic.on_action(player.get_pid(), self.received_data[DATA])
                    # if res[MSG_TYPE] == FINISH:
                    #     if self.game_end:
                    #         self.send_round_result(self.round_result)
                else:
                    # TODO: error case classification
                    pass
        except Exception as e:
            # TODO: error case classification
            pass
