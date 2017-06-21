import json
from server.string import *


class Message(object):
    def __init__(self, msg=None, msg_type=None, data=None, error_code=None):
        self.msg = msg
        self.msg_type = msg_type
        self.data = data
        self.error_code = error_code

    @classmethod
    def load_message(cls, json_data):
        try:
            parsed_dict = json.loads(json_data)
            keys = parsed_dict.keys()

            # initialize
            msg = None
            msg_type = None
            data = None

            if MSG in keys:
                msg = parsed_dict[MSG]
            if MSG_TYPE in keys:
                msg_type = parsed_dict[MSG_TYPE]
            if DATA in keys:
                data = parsed_dict[DATA]

            return cls(msg, msg_type, data)
        except json.JSONDecodeError:
            return cls()

    @staticmethod
    def dump_message(message):
        json_data = json.dumps(message.__dict__)
        return json_data

