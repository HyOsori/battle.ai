# -*- coding:utf-8 -*-
import json
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic

"""

<Dice Game 순서>
0. firstPhase = [0,0] >> p1, p2 모두 0으로 초기화
1. GameServer에서 onStart() 호출 >> 1. 시작, 0. 종료
2. 시작하면 TurnGameLogic.request() 호출
3. 그 뒤에 GameServer에서 onAction 호출할 때마다 request 호출 >> 재정의
4. 종료되어 onEnd() 호출 시 result() 호출하여 결과 전달

"""

class DiceGame(TurnGameLogic):
    def __init__(self, GameServer):  ## GameServer == TurnGameServer??
        # ## 0. 기권 1. 플레이
        TurnGameLogic.__init__(self, GameServer)
        self.msg_type = [0, 1]
        self.phaseList = [0, 0]

    def onStart(self, turn):
        print "Before changeTurn: ", self.turnNum
        TurnGameLogic.onStart(self, turn)
        print "After changeTurn: ", self.turnNum

        #self.messageList = self.msg_type
        print "Current phaseList: ", self.phaseList
        game_data = {"game_data" : self.phaseList}
        self.request(turn[0], 1, game_data)

    def onAction(self, pid, json_data):
        try:
            if not pid == self.playerList[self.turnNum]:
                return False

            message = json.loads(json_data)
            msg = message["msg"]
            if not msg == "game_data":
                return False

            game_data = message["game_data"]
            # in dice game, game_data = {"num": (num)}
            # check rule, calculate score and change turn
            if game_data["num"] > 6 | game_data["num"] < 1:
                return False

            self.game_data[self.turnNum] += game_data["num"]
            self.changeTurn()

            # send next request
            self.request(self.playerList[self.turnNum], 1, self.game_data)

            return True

        except Exception as e:
            print e
            return False

    def onError(self, pid):
        pass

    def onEnd(self):
        self.result(self.phaseList)

    def calculate_score(self, turn_num, game_data):
        self.phaseList[turn_num] += game_data

    def result(self, score_list):
        if score_list[0] > score_list[1]:
            print("P1 WIN")
            pass
        elif score_list[0] < score_list[1]:
            print("P2 WIN")
            pass
        else:
            print("DRAW")
            pass
