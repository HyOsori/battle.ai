import json
from server.m_format import *
from tornado import gen
import tornado.ioloop
from functools import partial

buffer_size = 50000

class User:
    def __init__(self, conn):
        self.conn = conn
        self.io_loop = tornado.ioloop.IOLoop.instance()

    def _trim(self, string):
        return string.replace(" ", "")

class Player(User):
    def __init__(self, pid, conn):
        User.__init__(self, conn)
        self.pid = pid
        self.playing = False

    def __error_callback(self, future):
        future.set_exception(gen.TimeoutError("Timeout"))

    @gen.coroutine
    def timeout_read(self, timeout=10):
        future = self.conn.read_bytes(buffer_size, partial=True)
        timeout_handle = self.io_loop.add_timeout(self.io_loop.time() + timeout, partial(self.__error_callback, future=future))
        future.add_done_callback(lambda r: self.io_loop.remove_timeout(timeout_handle))
        message = yield future
        raise gen.Return(message)

    def read(self):
        return self.conn.read_bytes(buffer_size, partial=True)

    def get_pid(self):
        return self.pid

    def send(self, data):
        try:
            self.conn.write(self._trim(data))
        except Exception as e:
            print "player bye bye"
            print e


class Attendee(User):
    def __init__(self, conn):
        User.__init__(self, conn)
        self.attendee_flag = True

    def notice_user_added(self, added_player):
        print "notice user added ##"
        if self.attendee_flag:
            return

        msg = {MSG: NOTICE_USER_ADDED, USER: added_player}
        json_msg = json.dumps(msg)
        print json_msg

        self.send(self._trim(json_msg))

    def notice_user_removed(self, removed_player):
        print "notice user removed ##"
        if self.attendee_flag:
            return

        msg = {MSG: NOTICE_USER_REMOVED, USER: removed_player}
        json_msg = json.dumps(msg)

        self.send(self._trim(json_msg))

    def send(self, data):
        try:
            self.conn.write_message(self._trim(data))
        except Exception as e:
            print "attendee bye bye"+str(e)

    def room_enter(self):
        self.attendee_flag = True

    def room_out(self):
        self.attendee_flag = False
