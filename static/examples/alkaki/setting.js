var setting = new Object();

//Edit Start-------------------------------------------------------------
setting.title = "Alkaki"; //name of game

setting.use_animation = true;

setting.max_match_cnt = 2; //max num of players can match
setting.min_match_cnt = 2; //min num of players can match

setting.use_gameBoard_chart = false;

setting.protocol = {
    "response_user_list" : Lobby.renewPlayerList,
    "notice_user_added" : Lobby.addPlayer,
    "notice_user_removed" : Lobby.removePlayer,
    "response_match" : Lobby.getMatchResponse,
    "game_handler" : {
        "ready" : GameBoard.gameStart,
        "end" : GameResult.recvGameResult
    },
    "game_data" : { //this msg can be changed according to game
        "game" : GameBoard.recvTurnResult
    } 
};