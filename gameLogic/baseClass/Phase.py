class Phase(object):
    def __init__(self, logic_server, message_type):
        self._logic_server = logic_server
        self.messageType = message_type
        self.notify_message_type = 'notify_' + message_type
        self.notify_init_message_type = 'notify_init_' + message_type
        self.notify_finish_message_type = 'notify_finish_' + message_type

    def on_start(self):
        pass

    def do_action(self, pid, dict_data):
        return True

    def on_end(self):
        pass

    def change_phase(self, index):
        self._logic_server.change_phase(index)

    def change_turn(self, index=None):
        self._logic_server.change_turn(index)

    def now_turn(self):
        return self._logic_server.now_turn()

    def request(self, pid, dict_data):
        self._logic_server.request(pid, self.messageType, dict_data)

    def request_all(self, dict_data):
        self._logic_server.request_all(self.messageType, dict_data)

    def end(self, is_valid_end, result_list=None):
        self._logic_server.end(is_valid_end, result_list)

    def get_shared_dict(self):
        return self._logic_server.get_shared_dict()

    def get_player_list(self):
        return self._logic_server.get_player_list()

    def set_player_result(self, pid, result):
        self._logic_server.set_player_result(pid, result)

    def set_all_player_result(self, result):
        self._logic_server.set_all_player_result(result)

    def get_player_result(self, pid):
        return self._logic_server.get_player_result(pid)

    def notify(self, dict_data):
        self._logic_server.notify(self.notify_message_type, dict_data)

    def notify_init(self, dict_data):
        self._logic_server.notify(self.notify_init_message_type, dict_data)

    def notify_finish(self, dict_data):
        self._logic_server.notify(self.notify_finish_message_type, dict_data)

    def notify_free(self, notify_message_type, dict_data):
        self._logic_server.notify(notify_message_type, dict_data)
