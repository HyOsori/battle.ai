# -*- coding:utf-8 -*-


class AIParser(object):
    def __init__(self):
        """
        :return: None
        """
        self._client = None
        self.pid = None
        self.msg = None
        self.msg_type = None
        self.game_data = None

    def init_parser(self, client, username):
        """
        :param client: Client class, client calls this function to initialize parser
        :param username: client's username
        :return: None
        """
        self._client = client
        self.pid = username

    # game_data 로는 room에서 보낸 json이 loads된 상태의 dict 자료형이 반환된다.
    # dict자료형에 대한 정보는 문서를 참조하며, 그 dict의 정보를 활용하여 logic을 실행 시킨다.
    # 그리고 반환형에 맞춰서 정보를 조작한후 리턴한다.

    # 고로 이 부분이 사용자가 코딩할 부분!

    def decoding(self, decoding_data):
        """
        :param decoding_data: received data from server (dict)
        :return: None
        """
        self.msg = decoding_data['msg']
        self.msg_type = decoding_data['msg_type']
        self.game_data = decoding_data['data']

    def parsing_data(self, decoding_data):
        """
        :param decoding_data: Received data from server (dict)
        :return: response of AI client (dict)
        """
        self.decoding(decoding_data)
        ret = None
        if self.msg_type == 'init':
            ret = self.init_phase()
        elif self.msg_type == 'finish':
            ret = self.finish_phase()
        elif self.msg_type == 'round_result':
            ret = {'response': 'OK'}
        elif self.msg_type == 'ready':
            ret = {'response' : 'OK'}
        # temporary implemenation ;; must be del
        elif self.msg_type == 'game_result':
            ret = {'response' : 'OK'}
        if ret != None:
            ret = self.make_send_msg(self.msg_type, ret)
        return ret

    @staticmethod
    def make_send_msg(msg_type, game_data):
        """
        :param msg_type: Type of message to send (string)
        :param game_data: Game data to send(dict)
        :return: response of AI client (dict)
        """
        # 서버와 통신이 가능한 프로토콜로 포장하는 역할을 하는 메소드
        send_msg = {"msg": "game_data"}
        if msg_type == 'ready':
            send_msg["msg"] = "game_handler"
        send_msg["msg_type"] = msg_type
        send_msg["data"] = game_data
        return send_msg

    def init_phase(self):
        """
        :return: response of AI client (dict)
        """
        parsing_data = dict()
        parsing_data['response'] = 'OK'
        send_msg = self.make_send_msg(self.msg_type, parsing_data)
        return send_msg

    def finish_phase(self):
        """
        :return: response of AI client (dict)
        """
        parsing_data = dict()
        parsing_data['response'] = 'OK'
        send_msg = self.make_send_msg(self.msg_type, parsing_data)
        return send_msg
