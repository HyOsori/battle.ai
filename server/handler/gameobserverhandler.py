import json
import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
from server.gameobject.room import Room

from server.handler.turngamehandler import TurnGameHandler
from server.string import *
from server.gameobject.user import Observer
from server.pools.user_pool import UserPool
from server.gameobject.message import Message


# TODO: get db connection by self.application.db
class GameObserverHandler(tornado.websocket.WebSocketHandler):
    # def __init__(self):
    #     logging.debug("ObserverHandler __init__ is called")
    #     self.__instance = None
    #     pass

    def initialize(self):
        print("ObserverHandler initialize is called")
        pass

    def open(self, *args, **kwargs):
        '''
        open websocket
        '''
        print("ObserverHandler open is called " + str(self))

        observer = Observer(self)

        observer_pool = UserPool.instance().get_observer_pool()
        observer_pool.add_observer(observer)

        self.__instance = observer

    def on_message(self, message):
        '''
        When receive message from Attendee, this function runs.
        :param message: message from Attendee
        '''
        print(message)

        message = Message.load_message(message)

        # TODO: gamehandler rename ..
        if message.msg == "gamehandler":
            if message.msg_type == MATCH:
                self.handle_match(message.data)

    def handle_match(self, data):
        match_type = data["type"]
        print("handle_match is called with type: " + match_type);

        if match_type == GAME_LOG:
            self.handle_gamelog_match(data["_id"])
        elif match_type == USER:
            self.handle_user_match(data["players"])

    def handle_user_match(self, players):
        print("handle_user_match is called with players: " + str(players))
        player_pool = UserPool.instance().get_player_pool()

        # set matched player flag on!
        try:
            match_players = []
            _ids = players
            for _id in _ids:
                player = player_pool.get_player(_id)
                player.room_enter()
                match_players.append(player)
        except Exception as e:
            print(e)
            return

        observer_pool = UserPool.instance().get_observer_pool()
        for pid in _ids:
            for observer in observer_pool:
                observer.notice_user_removed(pid)
        try:
            room = Room(match_players)
            room.add_observer(self.__instance)

            game = TurnGameHandler(room)
        except Exception as e:
            print(e)
            return

        # run game
        tornado.ioloop.IOLoop.current().spawn_callback(game.run)

        data = Message.dump_message(
            Message(RESPONSE_ + MATCH, None, {USERS: _ids}))

        try:
            self.write_message(data)
            self.__instance.room_enter()
        except Exception as e:
            print(e)
            observer_pool.pop(self.__instance)


    def handle_gamelog_match(self, _id):
        pass

    def _response_user_list(self):

        self.__instance.observer_flag = False

        player_pool = UserPool.instance().get_player_pool()

        runnable_players = []
        for player in player_pool:
            if not player.playing:
                runnable_players.append(player._id)

        # message = Message(RESPONSE_ + USER_LIST, None,
        # 다른 key value 에 대해서도 kwarg 로 저장가능하도록 하기
        msg = {MSG: RESPONSE_ + USER_LIST, USERS: runnable_players}
        json_msg = json.dumps(msg)

        try:
            self.write_message(json_msg)
        except Exception:
            observer_pool = UserPool.instance().get_observer_pool()
            observer_pool.pop(self.__instance)

    def _response_match(self, data):
        player_pool = UserPool.instance().get_player_pool()

        # set matched player flag on!
        try:
            match_players = []
            _ids = data[USERS]
            for _id in _ids:
                player = player_pool.get_player(_id)
                player.room_enter()
                match_players.append(player)
        except Exception:
            return

        observer_pool = UserPool.instance().get_observer_pool()

        for pid in _ids:
            for observer in observer_pool:
                observer.notice_user_removed(pid)
        try:
            room = Room(match_players)
            room.add_observer(self.__instance)

            game = TurnGameHandler(room)
        except Exception:
            return

        # run game
        tornado.ioloop.IOLoop.current().spawn_callback(game.run)
        speed_list = [0.5, 0.3, 0.1, 0.05, 0]

        data = Message.dump_message(Message(RESPONSE_ + MATCH, None, {USERS: data[USERS], ERROR: 0, SPEED: speed_list[int(data[SPEED])]}))

        try:
            self.write_message(data)
            self.__instance.room_enter()
        except Exception:
            observer_pool.pop(self.__instance)

    # TODO : find out how to deal with this error (CORS)
    def check_origin(self, origin):
        return True

    def on_close(self):
        observer_pool = UserPool.instance().get_observer_pool()
        observer_pool.remove_observer(self.__instance)
