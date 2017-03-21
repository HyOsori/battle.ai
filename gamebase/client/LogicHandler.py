from gamebase.client.string import *


class LogicHandler(object):
    def __init__(self):
        pass

    def handle_message(self, received_msg):
        msg = received_msg[MSG]
        msg_type = received_msg[MSG_TYPE]
        message = received_msg[DATA]

        print(msg, msg_type, message)
        if msg == GAME_HANDLER:
            if msg_type == READY:
                msg_type, data = self.init_phase(msg_type, message)
                message = {MSG: GAME_HANDLER, MSG_TYPE: msg_type, DATA: data}
            elif msg_type == END:
                return
        elif msg == GAME_DATA:
            msg_type, data = self.loop_phase(msg_type, message)
            message = {MSG: GAME_DATA, MSG_TYPE: msg_type, DATA: data}
        else:
            print("Unexpected message is come from server")
            return
        print(message)
        return message

    def init_phase(self, msg_type, data):
        raise NotImplementedError

    def loop_phase(self, msg_type, data):
        raise NotImplementedError
