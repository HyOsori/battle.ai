var setting = new Object();

//Edit Start-------------------------------------------------------------
setting.title = "battle.ai"; //name of game

setting.max_match_cnt = 2; //max num of players can match
setting.min_match_cnt = 2; //min num of players can match

setting.protocol = {
    "response_user_list" : renewPlayerList, //lobby
    "notice_user_added" : addPlayer, //lobby
    "notice_user_removed" : removePlayer, //lobby
    "response_match" : getMatchResponse, //lobby
    "game_handler" : {
        "ready" : gameStart, //gameBoard
        "end" : recvGameResult //gameResult
    },
    "game_data" : recvTurnResult //gameBoard (this msg can be changed according to game)
};