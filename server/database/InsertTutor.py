# -*- coding: utf-8 -*-
from server.database.MysqlDriver import LogDB

db_base = LogDB()

# LogDB.add_game_log(db_base,'winner', 5, 'loser', 3)
# default cnt = 1, name = 'none', win_lose = 'all'
# print LogDB.search_game_log(db_base,cnt=3,name='hi',win_lose='win');
# print LogDB.search_game_log(db_base)

# message = {MSG: GAME_LOG, MSG_TYPE: REQUEST_LOG_DATA, DATA: [cnt, name, win_lose]}
# message = {MSG: GAME_LOG, MSG_TYPE: RESPONSE_LOG_DATA, DATA: [[winner, win_score, loser, lose_score]]}
