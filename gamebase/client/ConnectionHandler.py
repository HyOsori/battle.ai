import json
import socket
from gamebase.client.string import *

BUFFER_SIZE = 256


class ConnectionHandler(object):
    def __init__(self):
        self.conn = None
        pass

    def connect(self, address, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((address, port))
            print("Success on connection")
            return True
        except IOError:
            return False

    def register_username(self, username):
        data = {USERNAME: username}
        message = {MSG: USER_INFO, MSG_TYPE: INIT, DATA: data}

        message = json.dumps(message)
        self.conn.send(message.encode())

        message = self.conn.recv(BUFFER_SIZE)
        message = json.loads(message.decode())
        data = message[DATA]

        print(data)
        if data[RESPONSE] == OK:
            return True
        else:
            return False

    def receive_data(self):
        message = self.conn.recv(BUFFER_SIZE)
        message = json.loads(message.decode())

        return message

    def send_data(self, message):
        message = json.dumps(message).encode()
        self.conn.send(message)

