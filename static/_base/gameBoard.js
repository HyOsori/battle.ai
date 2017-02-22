var GameBoard = new Object();

//load elements-----------------------------------------------------
GameBoard.canvas = document.getElementById("id_gameBoard_canvas");

GameBoard.canvas_text_size = 15;
GameBoard.canvas_text_interval = 1.3;

GameBoard.turn = 0;

//basic functions for gameBoard------------------------------------------
GameBoard.gameStart = function() {
    GameBoard.turn = 0;
    resizeCanvas(GameBoard.canvas);
    clearCanvas(GameBoard.canvas);
}

GameBoard.recvTurnResult = function(JSON_data) {
    ++GameBoard.turn;

    drawText(GameBoard.canvas, JSONtoString(JSON_data.data), GameBoard.canvas_text_size, 
             -1, GameBoard.turn * GameBoard.canvas_text_size * GameBoard.canvas_text_interval);
}