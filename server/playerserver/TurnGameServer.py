#-*- coding:utf-8 -*-
import json
from server.m_format import *
from tornado import gen
from gameLogic.baskin.baskinServer import BaskinServer
from server.playerserver.GameServer import GameServer


class TurnGameServer(GameServer):
    def __init__(self, room, battle_ai_list, web_client_list, game_logic = None):
        game_logic = BaskinServer(self)
        GameServer.__init__(self, room, battle_ai_list, web_client_list, game_logic)

    @gen.coroutine
    def _player_handler(self, player):
        try:
            print player.get_pid()+"!! Player handler running"

            while True:
                message = yield player.read()
                res = json.loads(message)
                print res
                if res[MSG_TYPE] == self.current_msg_type:
                    self.delay_action()
                    self.game_logic.onAction(player.get_pid(), res[GAME_DATA])
                    if res[MSG_TYPE] == FINISH:
                        self.q.get()
                        self.q.task_done()
                        break
                else:
                    self.game_logic.onError(player.get_pid())
                    self.q.get()
                    self.q.task_done()
                    break
                    # raise Exception
            print "player END!!!!!"
        except Exception as e:
            self.game_logic.onError(player.get_pid())
            self.q.get()
            self.q.task_done()
            print "[!] ERROR : " + e
