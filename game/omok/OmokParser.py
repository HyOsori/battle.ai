#-*-coding:utf-8-*-
import sys

from gamebase.client.AIParser import AIParser

import utils.debugger as logging

sys.path.insert(0,'../')


class OMOKParser(AIParser):
    def __init__(self):
        self._client = None
        self.pid = None
        self.msg = None
        self.msg_type = None
        self.game_data = None

        self.width = None
        self.height = None
        self.board = None

    def init_parser(self, client, username):
        """
        :param client: Client class, client calls this function to initialize parser
        :param username: client's username
        """
        self._client = client
        self.pid = username

    # game_data 로는 room 에서 보낸 json 이 loads 된 상태의 dict 자료형이 반환된다.
    # dict 자료형에 대한 정보는 문서를 참조하며, 그 dict 의 정보를 활용하여 logic 을 실행 시킨다.
    # 그리고 반환형에 맞춰서 정보를 조작한후 리턴한다.

    # 고로 이 부분이 사용자가 코딩할 부분!

    def decoding(self, decoding_data):
        """
        :param decoding_data: received data from server (dict)
        """
        self.msg = decoding_data['msg']
        self.msg_type = decoding_data['msg_type']
        self.game_data = decoding_data['data']

    def parsing_data(self, decoding_data):
        base = super(OMOKParser, self).parsing_data(decoding_data)
        logging.debug(str(decoding_data))
        ret = None

        if self.msg_type == 'loop':
            ret = self.loop_phase(self.game_data["board"])

        # elif self.msg_type == 'notify_init_loop':
        #    self.notify_loop_init()
        # elif self.msg_type == 'notify_change_round':
        #    self.notify_change_round()

        if ret is None:
            return base
        else:
            return self.make_send_msg(self.msg_type, ret)

    def loop_phase(self):
        # ![OVERRIDE] return loop result user's parser
        raise NotImplementedError

    def init_phase(self):
        raise NotImplementedError

    def finish_phase(self):
        """
        :return: response of AI client (dict)
        """
        parsing_data = dict()
        parsing_data['response'] = 'OK'
        send_msg = self.make_send_msg(self.msg_type, parsing_data)
        return send_msg
