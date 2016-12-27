# -*- coding:utf-8 -*-
from socket import *
import json
import zlib

# 사용자가 tcp 소켓에 신경 쓰지 않고 클라이언트를 제작 할수
#있도록 주요 함수들을 제공하자.

# 클라이언트 생성시 소켓 연결
import AIParser

# 사용자는 자신의 게임에 맞는 client와 parser를 구현하는게 아니라
# 자신의 게임의 맞는 parser만 구현하면 되게 만들자!


class Client(object):
    def __init__(self):
        self._sock = None
        self._parser = None
        self.__remain_packet = ""

    def connect_server(self, host, port):
        self._sock = socket(AF_INET, SOCK_STREAM)
        try:
            self._sock.connect((host, port))
        except socket.error:
            print '연결에 실패 하였습니다.'
            return False

        print '서버에 연결 되었습니다.'

        self.set_send_username()

    def __del__(self):
        self._sock.close()

    def get_username(self):
        return self._username

    def set_parser(self, parser):
        parser.init_parser(self, self._username)
        self._parser = parser

    # user name을 룸이 받는 프로토콜을 확인한후에 작성 할것
    def set_send_username(self):
        print '사용할 닉네임을 결정 하세요.'
        self._username = raw_input()

        if self._username == 'None':
            print 'None이라는 닉네임은 사용하면 안됌'
            self.set_send_username()
            return

        send_msg = {}
        send_msg['msg'] = 'user_info'
        send_msg['msg_tpye'] = 'init'
        send_msg['data'] = {'username' : self._username}
        json_msg = json.dumps(send_msg)
        self._sock.send(json_msg)

    # 데이터가 따로 오는 경우 처리를 해야함
    def recv_game_data(self):
        print 'waiting...'
        if self.__remain_packet == "":
            game_data = self._sock.recv(18000)

            cnt_open_brace = 0
            i = 0
            while i < len(game_data):
                if game_data[i] == '{':
                    cnt_open_brace += 1
                elif game_data[i] == '}':
                    cnt_open_brace -= 1
                    if cnt_open_brace == 0:
                        break
                i += 1

            # JSON 하나 자르고 남은 것이 있는 상태
            if i < len(game_data) - 1:
                self.__remain_packet = game_data[i + 1:]
                game_data = game_data[:i + 1]
                print 'cut game_data', game_data
                decoding_data = json.loads(game_data)
                return decoding_data
            # 딱 떨어지는 JSON을 받음
            elif i == len(game_data) - 1:
                self.__remain_packet = ""
                decoding_data = json.loads(game_data)
                print 'recv :\n', decoding_data
                return decoding_data
            # 미완성된 JSON을 받아놓은 상태
            else:
                self.__remain_packet = game_data[i + 1:]

        while True:
            cnt_open_brace = 0
            i = 0
            while i < len(self.__remain_packet):
                if self.__remain_packet[i] == '{':
                    cnt_open_brace += 1
                elif self.__remain_packet[i] == '}':
                    cnt_open_brace -= 1
                    if cnt_open_brace == 0:
                        break
                i += 1

            # JSON 하나 자르고 남은 것이 있는 상태
            if i < len(self.__remain_packet) - 1:
                game_data = self.__remain_packet[:i + 1]
                self.__remain_packet = self.__remain_packet[i + 1:]
                decoding_data = json.loads(game_data)
                return decoding_data
            # 딱 떨어지는 JSON을 받음
            elif i == len(self.__remain_packet) - 1:
                game_data = self.__remain_packet
                self.__remain_packet = ""
                decoding_data = json.loads(game_data)
                print 'recv :\n', decoding_data
                return decoding_data
            # 미완성된 JSON을 받아놓은 상태
            else:
                game_data = self._sock.recv(18000)
                print "seungmin", self.__remain_packet
                self.__remain_packet += game_data

                continue

    @staticmethod
    def make_send_msg(msg_type, game_data):
        send_msg = dict()
        send_msg["msg"] = "game_data"
        send_msg["msg_type"] = msg_type
        send_msg["data"] = game_data
        return send_msg

    # 인공지능 게임이 끝났을 때 정보를 받아야할까?
    def send_game_data(self, send_msg):
        if send_msg is None:
            return
        print "sending :"
        print send_msg
        self._sock.send(json.dumps(send_msg))

    # 클라이언트의 실행
    def client_run(self):
        if self._sock is None:
            print '소켓연결이 안되었습니다. connectServer(host, port)를 호출해주십시오'
            return
        if self._parser is None:
            print '파서가 등록이 안되있습니다.'
            return

        while True:
            decoding_data = self.recv_game_data()
            print decoding_data
            if decoding_data['msg'] == 'game_result':
                print decoding_data['data']
                continue
            send_msg = self._parser.parsing_data(decoding_data)
            self.send_game_data(send_msg)

    # 언제 while 루프를 벗어날까? 그런 신호가 하나 필요하겠다.??
