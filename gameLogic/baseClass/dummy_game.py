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
    TurnGameLogic.phaseList = [0, 0]  ## Default Phase

    def __init__(self, player):
        first_msg = [0, 1]  ## First MsgType
        TurnGameLogic.messageList = first_msg

        print("=====[INFO] GAME READY======")
        print("1. START")
        print("0. EXIT")

        # def requset(self, pid, messageType, JSON):
        #     self.room.requset(pid, messageType, JSON)

        choice = int(raw_input("CHOOSE NUMBER >> "))
        if choice == 1:
            ## 0. abstention
            ## 1. play DiceGame
            game_msg = [0, 1]
            TurnGameLogic.messageList = game_msg
            game_data = {"1":0}
            self.play_game(player, game_msg, game_data)
        elif choice == 0:
            self.__result(TurnGameLogic.phaseList)
            TurnGameLogic.onEnd()


    #### 재정의 부분 ####
    ## TurnGameLogic의 onAction 재정의
    def onAction(self,pid,args):
        self.play_game(pid, args)

    ## TurnGameLogic을 재정의
    def onEnd(self):
        self.result(TurnGameLogic.phaseList)

    def play_game(self, player, msg, data):
        TurnGameLogic.request(player, msg, data)
        self.calculate_score(player)  ## TODO: put in turn_num
        pass

    def calculate_score(self, player, turn_num):
        # TurnGameLogic.phaseList += player.score  ## TODO: keep adding player score
        pass

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

