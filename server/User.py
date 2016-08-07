import json
from server.m_format import *

class User:
    def __init__(self, conn):
        self.conn = conn

class Player(User):
    def __init__(self, pid, conn):
        User.__init__(self, conn)
        self.pid = pid

    def read(self):
        return self.conn.read_bytes(256, partial=True)

    def get_pid(self):
        return self.pid

    def send(self, data):
        self.conn.write(data)

class Attendee(User):
    def __init__(self, conn):
        User.__init__(self, conn)
        self.attendee_flag = True

    def notice_user_added(self, added_player):
        print "notice user added ##"
        if self.attendee_flag:
            return

        msg = {MSG: NOTICE+USER_ADDED, USER: added_player}
        json_msg = json.dumps(msg)
        self.conn.write_message(json_msg)
        print json_msg

    def notice_user_removed(self, removed_player):
        print "notice user added ##"
        if self.attendee_flag:
            return

        msg = {MSG: NOTICE + USER_REMOVED, USER: removed_player}
        json_msg = json.dumps(msg)
        self.conn.write_message(json_msg)

        print("notice message send!")

    def send(self, data):
        self.conn.write_message(data)

    def room_enter(self):
        self.attendee_flag = True

    def room_out(self):
        self.attendee_flag = False

        # What TO DO when Attendee exit, room send msg to Attendee
        # try - catch : solve it
