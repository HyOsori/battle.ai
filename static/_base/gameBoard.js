
//load elements-----------------------------------------------------
var gameBoard = document.getElementById("id_gameBoard_canvas");

var turn = 0;

//basic functions for gameBoard------------------------------------------
function gameStart() {
    resizeCanvas(gameBoard);
    clearCanvas(gameBoard);
}

function recvTurnResult(JSON_data) {
    ++turn;

    drawText(gameBoard, JSONtoString(JSON_data.data), -1, turn * 10);
}