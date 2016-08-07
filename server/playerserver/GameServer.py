#-*- coding:utf-8 -*-
from tornado import queues


"""
GAMESERVER(모든게임용)
TurnGameServer(턴게임용)

"""

class GameServer:
    def __init__(self, room, battle_ai_list, web_client_list, game_logic):
        self.game_logic = game_logic
        self.room = room
        self.battle_ai_list = battle_ai_list
        self.web_client_list = web_client_list
        self.current_msgtype = -1
        self.q = queues.Queue()

    def selectTurn(self, list):
        return [p.get_pid() for p in list]


    def perm(self, num):
        pass

    def save_game_data(self):
        pass
