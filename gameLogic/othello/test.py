#-*-coding:utf-8-*-
import sys
from gameLogic.baseClass.Client import Client
from gameLogic.othello.myOthelloParser import MyOthelloParser

HOST = '127.0.0.1'
PORT = 9001

client = Client()
if client.conntectServer(HOST,PORT) == False:
    print '서버 연결오류'
    sys.exit()
test1 = MyOthelloParser()
client.setParser(test1)

client.clientRun()
