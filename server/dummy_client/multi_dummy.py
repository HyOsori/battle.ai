#-*-coding:utf-8-*-
import threading
import zlib

class DummyManager:

    def __init__(self, parser, name, max_waiting_dummies = 1, max_dummies = 50):
        self.parser = parser
        self.name = name
        self.waitings = []
        self.gammings = []
        self.host = ''
        self.port = -1
        self.max_dummies = max_dummies
        self.max_waiting_dummies = max_waiting_dummies

    def attach(self, host, port):
        self.host = host
        self.port = port
        self._spawn_new_dummy()

    def _succeed_waiting(self, waited_dummy):
        if waited_dummy:
            self.waitings.remove(waited_dummy)
            self.gammings.append(waited_dummy)
        self._spawn_new_dummy()

    def _spawn_new_dummy(self):
        if len(self.waitings) >= self.max_waiting_dummies:
            raise Exception('There are too many waiting dummies') # TODO : raise exception
        if len(self.waitings)+len(self.gammings) >= self.max_dummies:
            raise Exception('There are too many dummies') # TODO : raise exception

        dummy = DummyClient()
        dummy.set_username(self.name)
        dummy.set_parser(parser=self.parser)
        dummy.connect_server(self.host, self.port)
        dummy.send_name()
        th = threading.Thread(target=dummy.client_run,
                              args=(self._succeed_waiting,
                                    lambda: self.gammings.remove(dummy)))
        dummy.th = th
        th.start()
        self.waitings.append(dummy)

    def kill_all_dummies(self, waitings=True, gammings=True):
        if waitings:
            for dummy in self.waitings:
                del dummy   #__del__ of dummy : release sock
            self.waitings = []
        if gammings:
            for dummy in self.gammings:
                del dummy
            self.gammings = []


    def join_all_dummies(self, waitings=True, gammings=True):
        pass

    # def get_waiting_dummies(self):
    #     pass
    #
    # def get_gaming_dummies(self):
    #     pass


from socket import *
import json


class DummyClient(object):
    def __init__(self):
        self._sock = None
        self._parser = None
        self.__remain_packet = "";
        self._username = 'Dummy'

    def connect_server(self, host, port):
        self._sock = socket(AF_INET, SOCK_STREAM)
        # try:
        self._sock.connect((host,port))
        # except:
        #     print '연결에 실패 하였습니다.'
            # return False
        print '서버에 연결 되었습니다.'

    def send_name(self):
        send_msg = {}
        send_msg['msg'] = 'user_info'
        send_msg['msg_tpye'] = 'init'
        send_msg['data'] = {'username': self._username}
        json_msg = json.dumps(send_msg)
        self._sock.send(json_msg)

    def __del__(self):
        self._sock.close()

    def set_username(self, name):
        self._username = name

    def set_parser(self, parser):
        parser.init_parser(self, self._username)
        self._parser = parser

    #데이터가 따로 오는 경우 처리를 해야함
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

            if i < len(game_data) - 1:  # JSON 하나 자르고 남은 것이 있는 상태
                self.__remain_packet = game_data[i + 1:]
                game_data = game_data[:i + 1]
                print 'cut game_data', game_data
                decoding_data = json.loads(game_data)
                return decoding_data
            elif i == len(game_data) - 1:  # 딱 떨어지는 JSON을 받음
                self.__remain_packet = ""
                decoding_data = json.loads(game_data)
                print 'recv :\n', decoding_data
                return decoding_data
            else:  # 미완성된 JSON을 받아놓은 상태
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

            if i < len(self.__remain_packet) - 1:  # JSON 하나 자르고 남은 것이 있는 상태
                game_data = self.__remain_packet[:i + 1]
                self.__remain_packet = self.__remain_packet[i + 1:]
                decoding_data = json.loads(game_data)
                return decoding_data
            elif i == len(self.__remain_packet) - 1:  # 딱 떨어지는 JSON을 받음
                game_data = self.__remain_packet
                self.__remain_packet = ""
                decoding_data = json.loads(game_data)
                print 'recv :\n', decoding_data
                return decoding_data
            else:  # 미완성된 JSON을 받아놓은 상태
                game_data = self._sock.recv(18000)
                print "seungmin", self.__remain_packet
                self.__remain_packet += game_data

                continue

    #이 부분도 그냥 Parser에 생성 해도 좋을듯
    def make_send_msg(self, msg_type, game_data):
        send_msg = {"msg": "game_data"}
        send_msg["msg_type"] = msg_type
        send_msg["data"] = game_data
        return send_msg

    #인공지능 게임이 끝났을 때 정보를 받아야할까?

    def send_game_data(self, send_msg):
        if send_msg == None:
            return
        print "sending :"
        print send_msg
        self._sock.send(json.dumps(send_msg))

    #클라이언트의 실행
    def client_run(self, on_new_game, on_end_game):
        if self._sock == None:
            print '소켓연결이 안되었습니다. connectServer(host, port)를 호출해주십시오'
            return
        if self._parser == None:
            print '파서가 등록이 안되있습니다.'
            return

        is_new_game = True
        while True:
            decoding_data = self.recv_game_data()
            if is_new_game and decoding_data['msg_type'] == 'ready':
                if on_new_game:
                    on_new_game(self)
                is_new_game = False
            if decoding_data['msg'] == 'game_result':
                print decoding_data['data']
                is_new_game = True
                if on_end_game:
                    on_end_game()
                break # 더미 클라이언트는 한번 붙고 종료
            send_msg = self._parser.parsing_data(decoding_data)
            self.send_game_data(send_msg)


