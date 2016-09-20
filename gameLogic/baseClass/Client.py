#-*-coding:utf-8-*-
from socket import *
import json

# 사용자가 tcp 소켓에 신경 쓰지 않고 클라이언트를 제작 할수
#있도록 주요 함수들을 제공하자.

# 클라이언트 생성시 소켓 연결
import gameDataParser

#사용자는 자신의 게임에 맞는 client와 parser를 구현하는게 아니라
#자신의 게임의 맞는 parser만 구현하면 되게 만들자!
class Client:
    def __init__(self):
        self._sock = None
        self._parser = None
        self.__remain_packet = "";

    def conntectServer(self, host, port):
        self._sock = socket(AF_INET, SOCK_STREAM)
        try:
            self._sock.connect((host,port))
        except:
            print '연결에 실패 하였습니다.'
            return False

        print '서버에 연결 되었습니다.'

        self.setAndSendUserName()


    def __del__(self):
        self._sock.close()

    def getUsername(self):
        return self._username

    def setParser(self,parser):
        parser.initParser(self,self._username)
        self._parser = parser

    #user name을 룸이 받는 프로토콜을 확인한후에 작성 할것
    def setAndSendUserName(self):
        print '사용할 닉네임을 결정 하세요.'
        self._username = raw_input()

        if self._username == 'None':
            print 'None이라는 닉네임은 사용하면 안됌'
            self.setAndSendUserName()
            return

        send_msg = {}
        send_msg['msg'] = 'user_info'
        send_msg['msg_tpye'] = 'init'
        send_msg['user_data'] = {'username' : self._username}
        json_msg = json.dumps(send_msg)
        self._sock.send(json_msg)

    #데이터가 따로 오는 경우 처리를 해야함
    def recvGameData(self):
        if self.__remain_packet == "":
            game_data = self._sock.recv(1024)

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
                print 'cut game_data', game_data
                decoding_data = json.loads(game_data)
                return decoding_data
            elif i == len(self.__remain_packet) - 1:  # 딱 떨어지는 JSON을 받음
                game_data = self.__remain_packet
                self.__remain_packet = ""
                decoding_data = json.loads(game_data)
                return decoding_data
            else:  # 미완성된 JSON을 받아놓은 상태
                game_data = self._sock.recv(1024)
                print "seungmin",self.__remain_packet
                self.__remain_packet += game_data

                continue

    #이 부분도 그냥 Parser에 생성 해도 좋을듯
    def makeSendMsg(self, msg_type, game_data):
        send_msg = {"msg": "game_data"}
        send_msg["msg_type"] = msg_type
        send_msg["game_data"] = game_data
        return send_msg

    #인공지능 게임이 끝났을 때 정보를 받아야할까?

    def sendGameData(self, send_msg):
        if send_msg == None:
            return
        print "sending :"
        print send_msg
        self._sock.send(json.dumps(send_msg))

    #클라이언트의 실행
    def clientRun(self):
        if self._sock == None:
            print '소켓연결이 안되었습니다. connectServer(host, port)를 호출해주십시오'
            return
        if self._parser == None:
            print '파서가 등록이 안되있습니다.'
            return

        while True:
            decoding_data = self.recvGameData()
            if decoding_data['msg'] == 'game_result':
                print decoding_data['game_data']
                continue
            send_msg = self._parser.parsingGameData(decoding_data)
            self.sendGameData(send_msg)

    #언제 wihile 루프를 벗어날까? 그런 신호가 하나 필요하겠다.??
