#-*-coding:utf-8-*-
import sys

from game.pixels import MyPixelsParser2
from gamebase.client.Client import Client

#HOST = '104.199.218.103'
HOST = '127.0.0.1'
PORT = 9001

client = Client()
if client.connect_server(HOST, PORT) == False:
    print('서버 연결오류')
    sys.exit()
#test1 = MyPixelsParser()
test1 = MyPixelsParser2()
client.set_parser(test1)

client.client_run()
