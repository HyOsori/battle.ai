import json
from server.m_format import *

class User:
    def __init__(self, connect):
        self.connect = connect

    def conn(self):
        return self.connect

class Player(User):
    def __init__(self, pid, conn):
        User.__init__(conn)
        self.pid = pid

    def read(self):
        return self.conn.read_bytes(256, partial=True)


class Attendee(User):
    def __init__(self, connect):
        User.__init__(self, connect)

    def notice_user_added(self, added_player):
        msg = {MSG: NOTICE+USER_ADDED, USER: added_player}
        json_msg = json.dumps(msg)
        self.conn().write(json_msg)

    def notice_user_removed(self, removed_player):
        msg = {MSG: NOTICE + USER_REMOVED, USER: removed_player}
        json_msg = json.dumps(msg)
        self.conn().write(json_msg)

    def send(self, data):
        self.conn.write(data)

        # What TO DO when Attendee exit, room send msg to Attendee
        # try - catch : solve it
