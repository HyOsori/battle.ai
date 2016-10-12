#-*-coding:utf-8-*-
import sys
from gameLogic.baseClass.Client import Client
from gameLogic.othello.MyOthelloParser import MyOthelloParser
from gameLogic.othello.MyOthelloParser2 import MyOthelloParser2

HOST = '127.0.0.1'
PORT = 9001

client = Client()
if client.connect_server(HOST, PORT) == False:
    print '서버 연결오류'
    sys.exit()
test1 = MyOthelloParser2()
client.set_parser(test1)

client.client_run()
