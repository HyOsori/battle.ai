import utils.debugger as logging

# coding=utf-8


class TurnGameLogic(object):
    def __init__(self, game_server):
        self._game_server = game_server
        self._phase_list = []
        self._current_phase = None
        self._shared_dict = {}
        self._player_list = None
        self._turn_num = None
        self._message_type = None

    def on_ready(self, player_list):
        raise NotImplementedError

    def on_start(self):
        """
        Server Call When Game Start
        :return: void
        """
        logging.info("Game Phase")
        self._current_phase.do_start()

    def on_action(self, pid, dict_data):
        """
        Call Current Phase's do_action
        :param pid: user pid
        :param dict_data: game_dict_data
        :return: void
        """
        self._current_phase.do_action(pid, dict_data)

    def on_error(self, pid):
        pass

    def check_msg_type(self, received_msg_type):
        """
        game base 에서 준 msg type 이랑 현재 player 에게 받은
        msg type 이랑 비교 ㅇㅇ

        해서

        너가 준 request msg type 에 맞는 response msg type 인지 확인 후

        T/F 로 return gogo
        :param received_msg_type:
        :return:
        """
        pass

    def change_phase(self, index):
        """
        change_phase -> current phase's on_start
        :param index: phase index
        :return: void
        """
        if not (self._current_phase is None):
            self._current_phase.on_end()
        self._current_phase = self._phase_list[index]
        self._message_type = self._current_phase.message_type
        self._current_phase.do_start()

    def change_turn(self, index=None):
        """
        :param index: user number
        :return: void
        """
        if index is None:
            self._turn_num += 1
        else:
            self._turn_num = index

    def now_turn(self):
        """
        :return: now_turn player
        """
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

    def end(self, error_code, result_list=None):
        """
        send server "logic_server end"
        :param error_code: normal_end or error_code
        :param result_list:
        :return:
        """
        logging.debug(result_list)
        self._game_server.on_end(error_code, result_list)

    def append_phase(self, phase):
        """
        add phase to phase_list
        :param phase: phase to add
        :return:
        """
        self._phase_list.append(phase)
        return len(self._phase_list) - 1

    def get_shared_dict(self):
        return self._shared_dict

    def get_player_list(self):
        return self._player_list

    def notify(self, message_type, dict_data):
        """
        Send Data to Observer
        :param message_type:
        :param dict_data:
        :return:
        """
        self._game_server.notify(message_type, dict_data)
