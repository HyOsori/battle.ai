#-*- coding:utf-8 -*-
from tornado import queues


"""
GAMESERVER


"""

class GameServer:
    def __init__(self, room, battle_ai_list, game_logic):
        self.game_logic = game_logic
        self.room = room
        self.battle_ai_list = battle_ai_list
        self.current_msgtype = -1
        self.q = queues.Queue()


    def selectTurn(self, list):
        return [p.get_pid() for p in list]

    def perm(self, num):
        pass

    def __player_handler(self, player):
        print player.pid
        pass

    #
    # @gen.coroutine
    # def game_handler(self):
    #     try:
    #         turn = self.selectTurn(self.room.player_list)
    #         self.game_logic.onStart(turn)
    #
    #         print "on start is done"
    #         for player in self.room.player_list:
    #             self.q.put(player)
    #             self.__player_handler(player)
    #         yield self.q.join()
    #
    #     except:
    #         self.game_logic.onError()
    #         print('[ERROR] GAME SET FAILED')
    #     finally:
    #         print "END"
    #         self.game_logic.onEnd()

    def save_game_data(self):
        pass
