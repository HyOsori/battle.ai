#-*- coding:utf-8 -*-
import json

from server.m_format import *
from tornado import gen
from server.playerserver.GameServer import GameServer
from gameLogic.othello.OthelloGameLogic import OthelloGameLogic

import server.ServerLog as logging


class TurnGameServer(GameServer):
    def __init__(self, room, player_list, attendee_list, game_speed, game_logic = None):
        game_logic = OthelloGameLogic(self)
        GameServer.__init__(self, room, player_list, attendee_list, game_logic, game_speed)

    @gen.coroutine
    def _player_handler(self, player):
        logging.debug(str(self.delay_time)+" - delay time")
        try:
            print player.get_pid()+": Player handler running"
            while True:
                message = yield player.read()
                res = json.loads(message)
                print res
                if res[MSG_TYPE] == self.current_msg_type:
                    # correct message is come
                    yield self.delay_action()
                    self.game_logic.on_action(player.get_pid(), res[GAME_DATA])
                    print '_player_handler onAction is done'
                    if res[MSG_TYPE] == FINISH:
                        self.q.get()
                        self.q.task_done()
                        raise gen.Return(True)
                else:
                    # wrong message is come : kill player - finish all game
                    self.game_logic.on_error(player.get_pid())
                    self.normal_game_playing = False
                    for player in self.room.player_list:
                        yield self.q.get()
                        self.q.task_done()
                    logging.debug("in error case at player_handler")

        except Exception as e:
            # TODO : error correcting is needed in error case
            # wrong message is come : kill play - finish all game
            print e
            logging.error("wowowowowowowowowowowoo")
            self.game_logic.on_error(player.get_pid())
            self.normal_game_playing = False
            for player in self.room.player_list:
                yield self.q.get()
                self.q.task_done()
            logging.debug("in error case at player_handler (Exception)")
            # + remove player from room (and close that player's socket)

            # remove items from queue
