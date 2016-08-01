#-*- coding:utf-8 -*-
import json
from tornado import gen
from server.playerserver.GameServer import GameServer
from gameLogic.baseClass import TurnGameLogic
from gameLogic.baseClass.dummy_game import DiceGame

class TurnGameServer(GameServer):
    def __init__(self, room, battle_ai_list):
        game_logic = DiceGame(self)
        self.room = room
        GameServer.__init__(self, room, battle_ai_list, game_logic)

    @gen.coroutine
    def game_handler(self):
        try:
            turn = self.selectTurn(self.room.player_list)
            self.game_logic.onStart(turn)

            print "on start is done"
            for player in turn:
                self.q.put(player)
                self.__player_handler(player)
            yield self.q.join()
        except:
            self.game_logic.onError()
            print('[ERROR] GAME SET FAILED')
        finally:
            print "END"
            self.game_logic.onEnd()

    def request(self, player, msg, gameData):
        self.current_msgtype = msg

        print "check0"

        ##send
        data = { "msg" : "game_data", "msg_type" : msg , "game_data" : gameData }
        json_data = json.dumps(data)
        player.send(json_data)

        print "check 1"
        '''
        for attendee in self.room.attendee_list:
            attendee.send(json_data)
        '''
        print "request is done"

        # self.__player_handler(player)


    @gen.coroutine
    def __player_handler(self, player):
        while True:
            print "Player handler running"
            message = yield player.read()
            res = yield json.loads(message)
            if res["msg_type"] == self.current_msgtype:
                recv = TurnGameLogic.onAction(player, message)
                if not recv:
                    raise Exception
                else:
                    for attendee in self.room.attendee_list:
                        attendee.send(message)
            elif res["msg_type"] == "end":  ## end는 종료 메세지 타입
                self.q.get()
                self.q.task_done()
                break
            else:
                raise Exception
