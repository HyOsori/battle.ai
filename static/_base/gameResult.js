var GameResult = new Object();

//load elements-----------------------------------------------------
GameResult.resultBoard = document.getElementById("id_resultBoard_canvas");

GameResult.homeBtn = document.getElementById("id_goToLobby_btn");

//basic functions for gameResult------------------------------------------
GameResult.recvGameResult = function(JSON_data) {
    resizeCanvas(GameResult.resultBoard);
    loadPage("gameResult");
}