import json
from server.string import *
from tornado import gen
import tornado.ioloop
from functools import partial
import server.debugger as logging

buffer_size = 512


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

    def set_pid(self, pid):
        self.pid = pid

    def __error_callback(self, future):
        future.set_exception(gen.TimeoutError("Timeout"))

    @gen.coroutine
    def timeout_read(self, timeout=5):
        future = self.conn.read_bytes(buffer_size, partial=True)
        timeout_handle = self.io_loop.add_timeout(self.io_loop.time() + timeout, partial(self.__error_callback, future=future))
        future.add_done_callback(lambda r: self.io_loop.remove_timeout(timeout_handle))
        message = yield future
        return message.decode()

    @gen.coroutine
    def read(self):
        message = yield self.conn.read_bytes(buffer_size, partial=True)
        return message.decode()

    def get_pid(self):
        return self.pid

    def send(self, data):
        try:
            self.conn.write(data.encode())
        except Exception as e:
            logging.error(str(e))

    def room_enter(self):
        self.playing = True

    def room_out(self):
        self.playing = False


class Observer(User):
    def __init__(self, conn):
        User.__init__(self, conn)
        self.observer_flag = False

    def notice_user_added(self, added_player):
        if self.observer_flag:
            return

        msg = {MSG: NOTICE_USER_ADDED, USER: added_player}
        json_msg = json.dumps(msg)
        logging.info(json)

        self.send(json_msg)

    def notice_user_removed(self, removed_player):
        if self.observer_flag:
            return

        msg = {MSG: NOTICE_USER_REMOVED, USER: removed_player}
        json_msg = json.dumps(msg)

        self.send(json_msg)

    def send(self, data):
        try:
            self.conn.write_message(data)
        except Exception as e:
            logging.error(str(e))

    def room_enter(self):
        self.observer_flag = True

    def room_out(self):
        self.observer_flag = False


class LobbyUser(User):
    def __init__(self, conn):
        super().__init__(conn)


    def notify_gamelog_added(self):
        pass

    def notify_chat_sended(self):
        pass

    def notify_ai_added(self):
        pass

    def notify_ai_deleted(self):
        pass




