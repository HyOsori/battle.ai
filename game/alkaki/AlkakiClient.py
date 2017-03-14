# -*-coding:utf-8-*-
import sys

from gamebase.client.Client import Client

HOST = '127.0.0.1'
PORT = 9001

client = Client()
if client.connect_server(HOST, PORT) is False:
    print('서버 연결오류')
    sys.exit()

client.client_run()