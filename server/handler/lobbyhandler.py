import tornado.websocket
from server.string import *
from server.gameobject.message import Message
from server.db.dbhelper import DBHelper
from server.pools.user_pool import UserPool
from server.gameobject.user import LobbyUser

class LobbyHandler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        pass

    def open(self, *args, **kwargs):
        print("ObserverHandler open is called " + str(self))

        lobby_user = LobbyUser(self)

        lobby_pool = UserPool.instance().get_lobby_pool()
        lobby_pool.add_lobby_user(lobby_user)

        self.__instance = lobby_user

    def on_message(self, message):
        try:
            message = Message.load_message(message)

            msg = message.msg
            msg_type = message.msg_type
            data = message.data
        except Exception:
            # message paring error
            return

        # game log
        if msg == GAME_LOG:
            if msg_type == INIT:
                self.init_game_log()
                pass
        # chat
        elif msg == CHAT:
            if msg_type == SEND:
                self.notify_chat(data)
                pass
        elif msg == USER:
            if msg_type == INIT:

                pass

    def on_close(self):
        pass

    def init_game_log(self):
        db_helper = DBHelper.instance()

        game_log_list = db_helper.db.game_log_list.find({}, {"_id": True, "players": True, "game_result": True})

        result = list()
        for game_log in game_log_list:
            game_log["_id"] = str(game_log["_id"])
            result.append(game_log)

        message = Message(GAME_LOG, INIT, result)
        message = Message.dump_message(message)

        self.__instance.send(message)

    def notify_chat(self, data):
        message = Message()
        message.msg = CHAT
        message.msg_type = RECEIVE
        message.data = data

        message = Message.dump_message(message)

        lobby_user_pool = UserPool.instance().get_lobby_pool()
        for lobby_user in lobby_user_pool:
            lobby_user.send(message)

    def init_user_list(self):

        player_pool = UserPool.instance().get_player_pool()

        runnable_players = []
        for player in player_pool:
            if not player.playing:
                runnable_players.append(player._id)

        message = Message(USER, INIT, runnable_players)
        message = Message.dump_message(message)

        self.__instance.send(message)




