# -*- coding: utf-8 -*-
from server.database.MYSQL import LogDB

db_base = LogDB()

# LogDB.add_game_log(db_base,'winner', 5, 'loser', 3)
# default cnt = 1, name = 'none', win_lose = 'all'
# print LogDB.search_game_log(db_base,cnt=3,name='hi',win_lose='win');
# print LogDB.search_game_log(db_base)
