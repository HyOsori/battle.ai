from server.handler.dbhandler import DBHandler
import pymongo

IP = "localhost"
PORT = 9090


class MongoDBHandler(DBHandler):
    def __init__(self):
        self.conn = pymongo.MongoClient(IP, PORT)
        self.db = self.conn.playgrounddb

        pass

    def init_db(self):
        self.users = self.db.users
        self.game_log_list = self.db.game_log_list
    pass
