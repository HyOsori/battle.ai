# -*-coding:utf-8-*-
import sys

from game.omok.MyOmokParser import MyOMOKParser
from gamebase.client.Client import Client

# HOST = '104.199.218.103'
HOST = '127.0.0.1'
PORT = 9001

client = Client()
if client.connect_server(HOST, PORT) is False:
    print('서버 연결오류')
    sys.exit()

player_parser = MyOMOKParser()
client.set_parser(player_parser)

client.client_run()
