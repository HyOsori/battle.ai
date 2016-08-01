# -*- coding:utf-8 -*-
import json

from pip._vendor.distlib.compat import raw_input
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic
from tornado import gen

"""

<Dice Game 순서>
0. firstPhase = [0,0] >> p1, p2 모두 0으로 초기화
1. GameServer에서 onStart() 호출 >> 1. 시작, 0. 종료
2. 시작하면 TurnGameLogic.request() 호출
3. 그 뒤에 GameServer에서 onAction 호출할 때마다 request 호출 >> 재정의
4. 종료되어 onEnd() 호출 시 result() 호출하여 결과 전달

"""

# TurnGameLogic 생성자에 있는거~.,~
# self.room = room
# self.phaseList = [] >> 게임의 룰 (ex. 어떤 좌표에 돌을 놓는거..)
# self.messageList = []
# self.currentPhase = None
#

class DiceGame(TurnGameLogic):
    def __init__(self, GameServer):
        # ## 0. abstention
        ## 1. play DiceGame
        self.msg_type = [0, 1]
        TurnGameLogic.__init__(self, GameServer)
        self.phaseList = [0, 0]

    def onStart(self, turn):
        TurnGameLogic.onStart(self, turn)
        TurnGameLogic.messageList = self.msg_type
        print self.phaseList
        game_data = {"game_data" : self.phaseList}
        self.play_game(turn[0], 1, game_data)

    #####
    #### 재정의 부분 ####
    ## TurnGameLogic의 onAction 재정의
    def onAction(self,pid,args):
        data = json.loads(args)
        if pid == self.playerList[self.turnNum]:
            if data["msg"] == "game_data":
                print data["game_data"]
                print type(data["game_data"])
                if data["game_data"]["num"] <= 6:
                    self.calculate_score(self.turnNum, data["game_data"]["num"])
                    msg = {"score": self.phaseList}

                    print "before ", self.turnNum
                    self.turnNum = (self.turnNum + 1) % 2
                    print "after ", self.turnNum
                    pid = self.playerList[self.turnNum]

                    self.play_game(pid, 1, msg)
                    return True
                else:
                    return False
            else:
                pass
        else:
            ## 잘못됬다고 서버에 알려주기
            pass

    def onError(self, pid):
        pass

    ## TurnGameLogic을 재정의
    def onEnd(self):
        self.result(self.phaseList)

    def onError(self, pid):
        pass

    def play_game(self, player, msg, data):
        self.request(player, msg, data)

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

