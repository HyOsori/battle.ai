
#-*- coding:utf-8 -*-

from gameLogic.baseClass.dummy_game import DiceGame
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
    def __init__(self, room, battle_ai_list):
        self.game_logic = DiceGame
        self.room = room
        self.battle_ai_list = battle_ai_list
        self.current_msgtype = -1

    def selectTurn(self, list):
        # turn =
        # self.perm(0)
        return list

    def perm(self, num):
        pass

    @gen.coroutine
    def game_handler(self):
        try:
            turn = self.selectTurn(self.room.player_list)   #
            self.game_logic.onStart(turn)

            for player in self.room.player_list:
                turn.__player_handler(player)
        except:
            self.game_logic.onError()
            print('[ERROR] GAME SET FAILED')
        finally:
            self.game_logic.onEnd()

    def save_game_data(self):
        pass