import game.debugger as logging

# coding=utf-8
class TurnGameLogic(object):
    def __init__(self, game_server):
        self._game_server = game_server
        self._phase_list = []
        self._current_phase = None
        self._shared_dict = {}
        self._player_list = None
        self._result_dict = None
        self._turn_num = None
        self._message_type = None

    def on_ready(self, player_list):
        raise NotImplementedError

    def on_start(self):
        raise NotImplementedError


        '''
        서버에서 하나의 게임이 시작될때 호출 하는 callback 함수
        :param player_list: 서버에서 지정하는 사용자 리스트이다.
        :return: 없다.
        '''
        """
        self._player_list = player_list
        self._result_dict = dict(
            zip(player_list, ['draw'] * len(player_list))
        )
        self._turn_num = -1
        self.change_turn()"""

    def on_action(self, pid, dict_data):
        '''
        현재 phase의 do_action을 호출한다.
        :param pid: on_action을 요청할 사용자의 pid
        :param dict_data: on_action을 요청하면서 주는 부가정보
        :return: 없다.
        '''
        self._current_phase.do_action(pid, dict_data)

    def on_error(self, pid):
        pass

    def change_phase(self, index):
        '''
        주어진 phase를 현재 관리하는 phase로 지정한다.
        해당 phase의 on_start를 호출한다.
        :param index: phase이름을 인덱스로 준다.
        :return:
        '''
        if not (self._current_phase is None):
            self._current_phase.on_end()
        self._current_phase = self._phase_list[index]
        self._message_type = self._current_phase.message_type
        self._current_phase.on_start()

    def change_turn(self, index=None):
        '''
        게임의 턴을 순서상 다음 플레이어로 넘기거나 지정한 플레이어로 넘긴다.
        :param index:
        :return:
        '''
        if not (index is None):
            self._turn_num = index
        else:
            self._turn_num += 1

        while self._result_dict[self.now_turn()] == 'error':
            self._turn_num += 1

    def now_turn(self):
        '''
        현재 턴을 반환 한다.
        :return: 현재 턴
        '''
        length = len(self._player_list)
        return self._player_list[self._turn_num % length]

    def request(self, pid, message_type, dict_data):
        """
        해당 유저에게 message_type와 부가정보 dict_data에 맞는 반환을 요청한다.
        :param pid: 요청당할 사용자
        :param message_type: 요청하는 메시지
        :param dict_data: 요청할 때의 부가정보
        :return:
        """

        self._game_server.request(pid, message_type, dict_data)

    def request_all(self, message_type, dict_data):
        '''
        모든 플레이어에게 request한다.
        :param message_type:
        :param dict_data:
        :return:
        '''
        for pid in self._player_list:
            self.request(pid, message_type, dict_data)

    def end(self, error_code , result_list=None):
        '''
        서버의 on_end를 호출하여 logic server가 종료하였음을 알려준다.
        :param is_valid_end: 정상적인 종료였는지 아닌지 boolean 형태로 전해준다.
        :param result_list: 누가 이기고, 지고, 무승부 했는지 정보를 list 형태로 전해준다.
        :return:
        '''
        if not (result_list is None):
            result_list = self._result_dict

        self._game_server.on_end(error_code, result_list)

    def append_phase(self, phase):
        '''
        phase를 phase_list에 추가해준다.
        :param phase: 추가할 phase
        :return:
        '''
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
        '''
        사용자 또는 프론트에게 정보를 일방적으로 통보합니다.
        :param message_type:
        :param dict_data: 통보할 정보입니다.
        :return:
        '''
        self._game_server.notify(message_type, dict_data)
