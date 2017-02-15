
//load elements-----------------------------------------------------
var resultBoard = document.getElementById("id_resultBoard_canvas");

var homeBtn = document.getElementById("id_goToLobby_btn");

//basic functions for gameBoard------------------------------------------

function recvGameResult(JSON_data) {
    clearCanvas(resultBoard);
    loadPage("gameResult");
}

homeBtn.addEventListener("click", function() {
    loadPage("lobby");
});