var setting = new Object();

//Edit Start-------------------------------------------------------------
setting.title = "battle.ai"; //name of game

setting.max_match_cnt = 2;
setting.min_match_cnt = 2;

setting.protocol = {
    "gamelog" : Lobby.renewPlayerList,
    "chat" : Lobby.addPlayer
};