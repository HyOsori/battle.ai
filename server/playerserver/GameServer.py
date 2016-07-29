#-*- coding:utf-8 -*-

import json
# import GameLogic

from tornado import gen
from gameLogic.baseClass.dummy_GameLogic import dummy_GameLogic
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
        self.room = room
        self.current_msgtype = -1
        self.GameLogic = dummy_GameLogic(room)
        self.battle_ai_list = battle_ai_list

    def selectTurn(self):
        turn = []
        self.perm(0)
        return turn

    def perm(self, num):
        pass

    @gen.coroutine
    def game_handler(self):
        try:
            # turn = self.selectTurn()
            turn = self.room.player_list
            self.GameLogic.onStart(turn)
            for player in self.room.players:
                self.__player_handler(player)
        except:
            self.GameLogic.onError()
            print('[ERROR] GAME SET FAILED')
        finally:
            self.GameLogic.onEnd()

            for player in self.room.players:
                self.battle_ai_list[player.pid] = player
                for attendee in self.web_client_list.values():
                    attendee.notice_user_added(player.pid)

    def request(self, player, msg, gameData):
        self.current_msgtype = msg

        # send
        data = {"msg_type": msg, "game": gameData}
        json_data = json.dumps(data)
        player.send(json_data)
        for attendee in self.room.attendee_list:
            attendee.send(json_data)


    @gen.coroutine
    def __player_handler(self, player):
        while True:
            message = yield player.read()
            res = yield json.loads(message)
            if res["msg_type"] == self.current_msgtype:
                recv = self.GameLogic.onAction(player, message)
                if not recv:
                    raise Exception
                else:
                    for attendee in self.room.attendee_list:
                        attendee.send(message)
            elif res["msg_type"] == "end":  ## end는 종료 메세지 타입
                break
            else:
                raise Exception


    def save_game_data(self):
        pass



