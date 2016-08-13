#-*- coding:utf-8 -*-
import json
import time
from tornado import gen
from gameLogic.baskin.baskinServer import BaskinServer
from gameLogic.baseClass.dummy_game import DiceGame
from server.playerserver.GameServer import GameServer


class TurnGameServer(GameServer):
    def __init__(self, room, battle_ai_list, web_client_list):
        game_logic = BaskinServer(self)
        GameServer.__init__(self, room, battle_ai_list, web_client_list, game_logic)

    @gen.coroutine
    def _player_handler(self, player):

        print player.get_pid()+"!! Player handler running"

        while True:
            message = yield player.read()
            res = json.loads(message)
            print res
            if res["msg_type"] == self.current_msg_type:
                self.delay_action()
                self.game_logic.onAction(player.get_pid(), res['game_data'])
                if res["msg_type"] == 'finish':
                    print res
                    self.q.get()
                    self.q.task_done()
                    break
            else:
                raise Exception
        print "player END!!!!!"



