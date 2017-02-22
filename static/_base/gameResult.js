var GameResult = new Object();

//load elements-----------------------------------------------------
GameResult.canvas = document.getElementById("id_resultBoard_canvas");
GameResult.ctx = GameResult.canvas.getContext("2d");

GameResult.homeBtn = document.getElementById("id_goToLobby_btn");

//basic functions for gameResult------------------------------------------
GameResult.recvGameResult = function(JSON_data) {
    resizeCanvas(GameResult.canvas);
    loadPage("gameResult");
}