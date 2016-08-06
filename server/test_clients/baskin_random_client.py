#-*-coding:utf-8-*-
from socket import *
import json
from random import random



def request(msg_type, gmae_data):
	send_msg = {"msg" : "game_data"}
	send_msg["msg_data"] = msg_type
	send_msg["game_data"] = game_data
	sock.send(json.dumps(send_msg))


HOST = '127.0.0.1'
PORT = 8000

sock = socket(AF_INET, SOCK_STREAM)

try:
	sock.connect((HOST, PORT))
except:
	print '연결 에러'

print("연결 되었습니다.")

#send pid
print "username : "
username = raw_input()
sock.send(username)

min_n = 0
max_n = 0
finish_n = 0 

while True : 
	data = sock.recv(1024)
	json_data = json.loads(data)
	msg = json_data['msg']
	msg_type = json_data['msg_type'] 
	game_data = json_data['game_data']

	if(msg == 'game_result'):
		print msg_type, game_data[username]

	if msg_type == 'init':
		min_n = int(game_data['min'])
		max_n = int(game_data['max'])
		finish_n = int(game_data[finish_n])
		request(msg_type, {'response' : 'OK'})
	elif msg_type == 'gameloop':
		start_n = game_data['start']
		request(msg_type, {'num' : int(random()*(max_n+1-min_n)+min_n)})
	elif msg_type == 'finish':
		request(msg_type, {'response' : 'OK'})

	#모든 라운드가 종료되었다는게 필요
		#순대 4 매1 둑불 1 
