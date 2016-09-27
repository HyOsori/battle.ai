class TurnGameLogic(object):
	def __init__(self, game_server):
		self._game_server = game_server
		self._phase_list = []
		self._current_phase = None
		self._shared_dict = {}

	def on_start(self, player_list):
		self._player_list = player_list
		self._result_dict = dict(
			zip(player_list, ['draw'] * len(player_list))
			)
		self._turn_num = -1
		self.change_turn()

	def on_action(self, pid, dict_data):
		self._current_phase.do_action(pid, dict_data)

	def on_error(self, pid):
		pass

	def change_phase(self, index):
		if self._current_phase != None:
			self._current_phase.on_end()
		self._current_phase = self._phase_list[index]
		self._messageType = self._current_phase.messageType
		self._current_phase.on_start()

	def change_turn(self, index = None):
		if index != None:
			self._turn_num = index
		else:
			self._turn_num = self._turn_num + 1

		while self._result_dict[self.now_turn()] == 'error':
			self._turn_num = self._turn_num + 1

	def now_turn(self):
		length = len(self._player_list)
		return self._player_list[self._turn_num % length]

	def request_all(self, message_type, dict_data):
		for pid in self._player_list:
			self.request(pid, message_type, dict_data)

	def request(self, pid, message_type, dict_data):
		self._game_server.request(pid, message_type, dict_data)

	def end(self, is_valid_end, result_list=None):
		if result_list == None:
			result_list = self._result_dict
		
		self._game_server.on_end(is_valid_end, result_list)

	def append_phase(self, phase):
		self._phase_list.append(phase)
		return len(self._phase_list) - 1
		
	def get_shared_dict(self):
		return self._shared_dict

	def get_player_list(self):
		return self._player_list

	def set_player_result(self, pid, result):
		self._result_dict[pid] = result

	def set_all_player_result(self, result):
		for name, res in self._result_dict.iteritems():
			if res != 'error':
				self._result_dict[name] = result

	def get_player_result(self, pid):
		return self._result_dict[pid]

	def notify(self, message_type, dict_data):
		self._game_server.notify(message_type, dict_data)
