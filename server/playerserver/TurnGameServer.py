import json
from tornado import gen
from server.playerserver.GameServer import GameServer
from gameLogic.baseClass import TurnGameLogic

class TurnGameServer(GameServer):
    def __init__(self, room, battle_ai_list):
        GameServer.__init__(self, room, battle_ai_list)

    def request(self, player, msg, gameData):
        self.current_msgtype = msg

        ##send
        data = { "msg_type" : msg , "game" : gameData}
        json_data = json.dumps(data)
        player.send(json_data)
        for attendee in self.room.attendee_list:
            attendee.send(json_data)

        # self.__player_handler(player)


    @gen.coroutine
    def __player_handler(self, player):
        while True:
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
                break
            else:
                raise Exception
