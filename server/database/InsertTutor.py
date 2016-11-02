# -*- coding: utf-8 -*-
from server.database.MYSQL import LogDB


class InsertTutor:
    def __init__(self):
        self.db_base = LogDB()

    def insert_db(self, winner, win_score, loser, lose_score):
        LogDB.add_game_log(self.db_base, winner, win_score, loser, lose_score)

    def search_db(self, name):
        LogDB.search_game_log(self.db_base, name)

    def search_db_recent(self):
        LogDB.search_game_log_recent(self.db_base)

#a = InsertTutor()
#a.insert_db('qi', 3, 'pp', 2)
#a.search_db('hi')
#a.search_db_recent()