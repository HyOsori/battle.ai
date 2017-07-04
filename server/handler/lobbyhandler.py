import json
import tornado.websocket
from server.string import *
from server.gameobject.message import Message


class LobbyHandler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        pass

    def open(self, *args, **kwargs):
        pass

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
                pass
        # chat
        elif msg == CHAT:
            if msg_type == INIT:
                pass
            elif msg_type == SEND:
                pass
        elif msg == MATCH:
            if msg_type == REQUEST:
                # TODO: redirect game page
                pass

    def on_close(self):
        pass

    def init_game_log(self):
        pass

    def init_chat(self):
        pass

    def notify_chat(self):
        pass

    def request_match(self):
        pass




