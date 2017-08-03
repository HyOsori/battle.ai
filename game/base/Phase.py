import utils.debugger as logging


class Phase(object):
    def __init__(self, logic_server, message_type):
        self._logic_server = logic_server
        self.message_type = message_type
        self.notify_message_type = 'notify_' + message_type
        self.notify_init_message_type = 'notify_init_' + message_type
        self.notify_finish_message_type = 'notify_finish_' + message_type

    def do_start(self):
        raise NotImplementedError

    def do_action(self, pid, dict_data):
        raise NotImplementedError

    def change_phase(self, index):
        self._logic_server.change_phase(index)

    def change_turn(self, index=None):
        self._logic_server.change_turn(index)

    def now_turn(self):
        return self._logic_server.now_turn()

    def request(self, pid, dict_data):
        logging.info("send !!")
        self._logic_server.request(pid, self.message_type, dict_data)

    def end(self, error_code, result_list=None):
        self._logic_server.end(error_code, result_list)

    def get_shared_dict(self):
        return self._logic_server.get_shared_dict()

    def get_player_list(self):
        return self._logic_server.get_player_list()

    def notify(self, message_type, dict_data):
        self._logic_server.notify(message_type, dict_data)
