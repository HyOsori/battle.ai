from gamebase.client.ConnectionHandler import ConnectionHandler
from gamebase.client.string import *


ADDRESS = "127.0.0.1"
PORT = 9001
# PLAYER STATUS
ON_GAME = 1
WAITING = 2


class Player(object):
    def __init__(self, logic=None):
        self.conn = ConnectionHandler()
        self.logic = logic
        self.is_end = False
        self.username = None

    def learn_logic(self, logic):
        self.logic = logic

    def connect(self):
        return self.conn.connect(ADDRESS, PORT)

    def confirm_username(self, username):
        # send username to server
        # y: OK
        if self.conn.register_username(username):
            self.username = username
            return True
        # n: NO
        else:
            return False

    def play_game(self):
        while not self.is_end:
            message = self.conn.receive_data()
            print(message)
            if message[MSG_TYPE] == END:
                self.is_end = True
                self.print_end_status(message[ERROR_CODE])
            message = self.logic.handle_message(message)
            if message is not None:
                self.conn.send_data(message)

    def run(self):
        while True:
            self.play_game()
            self.is_end = False

    def print_end_status(self, status):
        if status is 0:
            print("normal end")
        elif 100 <= status < 200:
            print("logic error: " + status)
        elif 200 <= status < 300:
            print("socket error: " + status)
        elif 300 <= status < 400:
            print("wrong message: " + status)
        else:
            print("unexpected error occur")


def play(game_logic):
    player = Player()
    player.learn_logic(game_logic)
    if not player.logic:
        print("You must learn logic")
        return
    if not player.connect():
        print("Connection failure")
        return

    while True:
        username = input("Input your name: ")
        if player.confirm_username(username):
            print("Success in registering user name")
            break
        else:
            print("Failure to register user name")
    player.run()
