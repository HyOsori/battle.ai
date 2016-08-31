# -*-coding:utf-8-*-
from socket import *
import json
from random import random


def request(msg_type, game_data):
    send_msg = {"msg": "game_data"}
    send_msg["msg_type"] = msg_type
    send_msg["game_data"] = game_data
    print "sending :"
    print send_msg
    sock.send(json.dumps(send_msg))


HOST = '127.0.0.1'
PORT = 9001

sock = socket(AF_INET, SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
except:
    print '연결 에러'

print("연결 되었습니다.")

# send pid
print "username : "
# username = raw_input()
username = "테스터" + str(random())
tmp = {"msg": "user_info", "msg_type": "init", "user_data": {"username": username}}
tt = json.dumps(tmp)
sock.send(tt)

min_n = 0
max_n = 0
finish_n = 0

while True:
    data = sock.recv(1024)
    json_data = json.loads(data)
    msg = json_data['msg']
    msg_type = json_data['msg_type']
    print type(json_data)
    print "receiving : "
    print json_data
    game_data = json_data['game_data']

    if (msg == 'round_result'):
        print msg_type, game_data

    if msg_type == 'init':
        min_n = game_data['min']
        max_n = game_data['max']
        finish_n = game_data['finish']
        request(msg_type, {'response': 'OK'})
    elif msg_type == 'gameloop':
        start_n = game_data['start']
        r = int(random() * (max_n + 1 - min_n) + min_n)
        if start_n - 1 + r > finish_n:
            r = finish_n - start_n + 1
        print start_n, r
        request(msg_type, {'num': r})
    elif msg_type == 'finish':
        request(msg_type, {'response': 'OK'})

    # 모든 라운드가 종료되었다는게 필요
    # 순대 4 매1 둑불 1