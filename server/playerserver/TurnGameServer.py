#-*- coding:utf-8 -*-
import json
from tornado import gen
from gameLogic.baskin.baskinServer import BaskinServer
from gameLogic.baseClass.dummy_game import DiceGame
from server.playerserver.GameServer import GameServer

class TurnGameServer(GameServer):
    def __init__(self, room, battle_ai_list):
        game_logic = BaskinServer(self)
        self.room = room
        GameServer.__init__(self, room, battle_ai_list, game_logic)
        self.num = 0


    @gen.coroutine
    def game_handler(self):
        try:
            turns = [self.selectTurn(self.room.player_list)]
            for turn in turns:
                self.game_logic.onStart(turn)
                print "START"
                for player in self.room.player_list:
                    self.q.put(player)
                    self.__player_handler(player)
                yield self.q.join()
        except:
            self.game_logic.onError('test')
            print "[!] ERROR"
        finally:
            print "END"
            self.destroy_room()



    def request(self, pid, msg, gameData):
        # print 'request', player, msg, gameData
        for p in self.room.player_list:
            if p.get_pid() == pid:
                player = p
        self.current_msgtype = msg

        print player.get_pid()
        print player
        print "-----------------------"

        data = { "msg" : "game_data", "msg_type" : msg , "game_data" : json.loads(gameData) }
        json_data = json.dumps(data)

        try:
            player.send(json_data)
        except:
            print 'request : ', 'send error'



    ## front에 Logic이 전달
    def notify(self, msg, game_data):
        data = { "msg" : "game_data", "msg_type" : msg, "game_data" : game_data }
        json_data = json.dumps(data)

        for player in self.room.player_list:
            player.send(json_data)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)


    @gen.coroutine
    def __player_handler(self, player):
        print player.get_pid()
        while True:
            print "Player handler running"
            message = yield player.read()
            res = json.loads(message)
            print res
            if res["msg_type"] == self.current_msgtype:
                self.game_logic.onAction(player.get_pid(), json.dumps(res['game_data']))
                if res["msg_type"] == 'finish':
                    print res
                    self.q.get()
                    self.q.task_done()
                    break
            else:
                raise Exception


    def onEnd(self, isValidEnd, result, error_msg="none"):
        self.isValidEnd = isValidEnd
        self.result = result
        self.error_msg = error_msg

        # isValidEnd = normal_end
        if isValidEnd == True:
            data = {"msg": "round_result", "msg_type": isValidEnd, "game_data": result }
        elif isValidEnd == False:
            data = { "msg" : "game_result", "msg_type" : isValidEnd, "game_data" : result, "error_msg" : error_msg }

        json_data = json.dumps(data)

        for player in self.room.player_list:
            player.send(json_data)

        for attendee in self.room.attendee_list:
            attendee.send(json_data)


    def destroy_room(self):

        data = { "msg" : "game_result" , "msg_type" : self.isValidEnd, "game_data" : None, "error_msg" : self.error_msg }
        json_data = json.dumps(data)
        # for player in self.room.player_list:
        #     player.send(json_data)
        for attendee in self.room.attendee_list:
            attendee.send(json_data)


        for player in self.room.player_list:
            self.battle_ai_list[player.get_pid()] = player
            for attendee in self.room.attendee_list:
                attendee.notice_user_added(player.get_pid())

        for player in self.room.player_list:
            self.battle_ai_list[player.get_pid()] = player
            for attendee in self.room.attendee_list:
                attendee.notice_user_added(player.get_pid())

        for attendee in self.room.attendee_list:
            attendee.room_out()


