#-*-coding:utf-8-*-
from socket import *
import json

# 사용자가 tcp 소켓에 신경 쓰지 않고 클라이언트를 제작 할수
#있도록 주요 함수들을 제공하자.

# 클라이언트 생성시 소켓 연결
import gameDataParser

#사용자는 자신의 게임에 맞는 client와 parser를 구현하는게 아니라
#자신의 게임의 맞는 parser만 구현하면 되게 만들자!
class BaseClient:
    def __init__(self, host, port, parser):
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._parser = parser

        try:
            self._sock.connect((host,port))
        except:
            print '연결에 실패 하였습니다.'

        print '서버에 연결 되었습니다.'

    def __del__(self):
        self._sock.close()

    def sendUserName(self):
    #   self._username = raw_input()
    #  self._sock.send(self._username)
        pass

    def recvGameData(self):
        game_data = self._sock.recv(1024)
        decoding_data = json.loads(game_data)
        return decoding_data

    #이 부분도 그냥 Parser에 생성 해도 좋을듯
    def makeSendMsg(self, msg_type, game_data):
        send_msg = {"msg": "game_data"}
        send_msg["msg_type"] = msg_type
        send_msg["game_data"] = game_data
        return send_msg

    def sendGameData(self, send_msg):
        print "sending :"
        print send_msg
        self._sock.send(json.dumps(send_msg))

    def getSocket(self):
        return self._sock


    #클라이언트의 실행
    def clientRun(self):
        self.sendUserName()

        while True:
            decoding_data = self.recvGameData()
            parsing_data = self._parser.parsingGameData(decoding_data)
            self.sendGameData(parsing_data)

    #언제 wihile 루프를 벗어날까? 그런 신호가 하나 필요하겠다.