var setting = new Object();

//Edit Start-------------------------------------------------------------
setting.title = "battle.ai"; //name of game

setting.use_animation = false;

setting.max_match_cnt = 2; //max num of players can match
setting.min_match_cnt = 2; //min num of players can match

setting.protocol = {
    "response_user_list" : Lobby.renewPlayerList,
    "notice_user_added" : Lobby.addPlayer,
    "notice_user_removed" : Lobby.removePlayer,
    "response_match" : Lobby.getMatchResponse, 
    "game_handler" : {
        "ready" : GameBoard.gameStart, 
        "end" : GameResult.recvGameResult
    },
    "game_data" : GameBoard.recvTurnResult //this msg can be changed according to game
};