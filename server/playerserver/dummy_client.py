import socket

import json
import random


class Client:

    def __init__(self, pattern):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.pattern = pattern

    def __response(self):
        while True:
            received = self.client_sock.recv(256)
            print received

            message = json.loads(received)
            msg = message["msg"]
            msg_type = message["msg_type"]
            # game_data = message["game_data"]

            if msg == "game_data":
                if msg_type == 1:
                    s = {"msg": "game_data", "game_data": {"num": 6}}
                    s_data = json.dumps(s)
                    self.client_sock.send(s_data)
                    pass
                elif msg_type == 2:
                    s = {"msg": "game_data", "game_data": self.pattern[1]}
                    s_data = json.dumps(s)
                    self.client_sock.send(s_data)
                    pass
                elif msg_type == 3:
                    s = {"msg": "game_data", "game_data": self.pattern[2]}
                    s_data = json.dumps(s)
                    self.client_sock.send(s_data)
                    pass
                elif msg_type == "start":
                    print("Game start")
                elif msg_type == "end":
                    break

    def run(self):
        self.client_sock.connect(('127.0.0.1', 8000))

        print("input your name")
        msg = raw_input()
        self.client_sock.send(msg)

        self.__response()

client = Client([3, 5, 1])
client.run()
