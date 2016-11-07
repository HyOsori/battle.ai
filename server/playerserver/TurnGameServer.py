#-*- coding:utf-8 -*-
import json

from server.m_format import *
from tornado import gen
from server.playerserver.GameServer import GameServer
from gameLogic.othello.OthelloGameLogic import OthelloGameLogic
from gameLogic.pixels.PixelsGameLogic import PixelsGameLogic

import server.ServerLog as logging


class TurnGameServer(GameServer):
    def __init__(self, room, player_list, attendee_list, game_speed, game_logic = None, database = None):
        game_logic = PixelsGameLogic(self)
        GameServer.__init__(self, room, player_list, attendee_list, game_logic, game_speed, database)

    @gen.coroutine
    def _player_handler(self, player):
        logging.debug(str(self.delay_time)+" - delay time")
        try:
            print player.get_pid()+": Player handler running"
            while True:
                message = yield player.timeout_read()
                logging.debug("recv  "+message)
                res = json.loads(message)
                logging.debug(res[MSG_TYPE])
                logging.debug(self.current_msg_type)
                if res[MSG_TYPE] == self.current_msg_type:
                    if res[MSG_TYPE] == ROUND_RESULT:
                        logging.error("task done DONE")
                        self.q.get()
                        self.q.task_done()
                        break
                    # correct message is come
                    yield self.delay_action()
                    self.game_logic.on_action(player.get_pid(), res[DATA])
                    logging.info('_player_handler onAction is done')
                    if res[MSG_TYPE] == FINISH:
                        if self.game_end:
                            logging.debug("after on end, send round result")
                            self.send_round_result(self.round_result)
                        logging.debug("finish msg is come")
                else:
                    # wrong message is come : kill player - finish all game
                    self._exit_handler(player)
                    gen.Return(None)
                    logging.debug("in error case at player_handler")

        except Exception as e:
            # TODO : error correcting is needed in error case
            # wrong message is come : kill play - finish all game
            logging.error(e)
            logging.error("here???")
            if self.normal_game_playing:
                logging.error("wow")
                self._exit_handler(player)
            else:
                self.player_list[player.get_pid()] = player
            logging.debug("in error case at player_handler (Exception)")
            # + remove player from room (and close that player's socket)

            # remove items from queue
