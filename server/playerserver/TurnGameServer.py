#-*- coding:utf-8 -*-
import json
import time

from tornado.iostream import StreamClosedError

from server.m_format import *
from tornado import gen
from gameLogic.baskin.baskinServer import BaskinServer
from server.playerserver.GameServer import GameServer
from gameLogic.othello.OthelloGameLogic import OthelloGameLogic


class TurnGameServer(GameServer):
    def __init__(self, room, battle_ai_list, web_client_list, game_logic = None):
        game_logic = OthelloGameLogic(self)
        GameServer.__init__(self, room, battle_ai_list, web_client_list, game_logic)

    @gen.coroutine
    def _player_handler(self, player):
        try:
            print player.get_pid()+": Player handler running"

            while True:
                message = yield player.read()
                res = json.loads(message)
                print res
                if res[MSG_TYPE] == self.current_msg_type:
                    self.delay_action()
                    self.game_logic.on_action(player.get_pid(), res[GAME_DATA])
                    print '_player_handler onAction is done'
                    if res[MSG_TYPE] == FINISH:
                        self.q.get()
                        self.q.task_done()
                        break
                else:
                    self.game_logic.on_error(player.get_pid())
                    self.q.get()
                    self.q.task_done()
                    break
                    # raise Exception
            print "player END!!!!!"
        except Exception as e:
            print "player OUT!!!!!!!!!!!!!!!!!!!!!1 wow"
            self.game_logic.on_error(player.get_pid())

            # remove player from room and turns
            for turn in self.turns:
                try:
                    turn.remove(player.get_pid())
                except Exception as e:
                    print e
            print self.turns
            self.room.player_list.remove(player)

            yield self.q.get()
            #self.q.task_done()
            print "[!] ERROR : "
            print e
