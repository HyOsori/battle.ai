#-*-coding:utf-8-*-
from gameLogic.baseClass.baseClient import Client
from gameLogic.othello.myOthelloParser import MyOthelloParser

HOST = '127.0.0.1'
PORT = 9001

client = Client(HOST,PORT)
test1 = MyOthelloParser()
client.setParser(test1)

client.clientRun()