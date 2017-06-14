import json
import tornado.websocket
from server.string import *


class LobbyHandler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        pass

    def open(self, *args, **kwargs):
        pass

    def on_message(self, message):
        try:
            message = json.loads(message)

            msg = message[MSG]
            msg_type = message[MSG_TYPE]
            data = message[DATA]
        except Exception as e:
            # message paring error
            return

        # game log
        if msg == GAME_LOG:
            if msg_type == INIT:
                pass
        # chat
        elif msg == CHAT:
            if msg_type == INIT:
                pass
        elif msg == MATCH:
            if msg_type == REQUEST:
                pass
    def on_close(self):
        pass

    @staticmethod
    def init_game_log(user):
        pass


