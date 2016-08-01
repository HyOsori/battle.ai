
#-*- coding:utf-8 -*-

from gameLogic.baseClass import TurnGameLogic
from tornado import gen

"""
GAMESERVER

1. WebServer에서 web_client_list, battle_ai_list, Room을 전달 받는다
2. 생성자에서 게임 턴 순서 정하기 >> selectTurn() >> 순서 배열 리턴
3. onStart(pid[]) >> 게임 시작
4. request(pid, msgTyp, JSON게임판정보)으로 player와 logic에 전달
   msgType에 따른 적합성 판단 -> 유효범위의 msgType인지
5. onAction() 호출 >> 리턴값으로 유효성 전달받음
6. onError(), onEnd() 호출
7. 게임 진행에 따른 로그 저장 >> 일단 light하게 메모리에 저장

"""

class GameServer:
    def __init__(self, room):
        self.room = room
        self.current_msgtype = -1

    def selectTurn(self):
        turn = []
        self.perm(0)
        return turn

    def perm(self, num):
        num =1
        pass

    @gen.coroutine
    def __game_handler(self):
        try:
            turn = self.selectTurn(self.room.players)   #TODO : ~해야댐
            TurnGameLogic.onStart(turn)

            for player in self.room.players:
                turn.__player_handler(player)

        except:
            TurnGameLogic.onError()
            print('[ERROR] GAME SET FAILED')
        finally:
            TurnGameLogic.onEnd()

    def save_game_data(self):
        pass
