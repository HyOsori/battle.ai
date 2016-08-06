# -*- coding:utf-8 -*-
import json

from gameLogic.baseClass.TurnGameLogic import TurnGameLogic

"""
<Dice Game 순서>
0. game_data = [0,0] >> p1, p2 모두 0으로 초기화
1. GameServer에서 onStart() 호출 >> msg_type: 0-exit 1-play
2. 시작하면 TurnGameLogic.request() 호출
3. 그 뒤에 GameServer에서 onAction 호출할 때마다 request 호출 >> 재정의
4. 종료되어 onEnd() 호출 시 result() 호출하여 결과 전달
"""


class DiceGame(TurnGameLogic):
    def __init__(self, game_server):
        TurnGameLogic.__init__(self, game_server)
        self.game_data = [0, 0]
        self.all_round = 3
        self.cur_round = 0

    def onStart(self, players):
        TurnGameLogic.onStart(self, players)
        game_data = {"game_data": self.game_data}
        self.request(players[self.turnNum], 1, game_data)

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
        ##request로 결과 전달???

