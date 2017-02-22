var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var margin = 10;
var size = 8;
var interval = (canvas.width - (margin * 2)) / size;

var round = 1;
var canvas_size = $("#id_side").css('height');
var users;
var x, y, nowTurn;

function ReadyAfterResize() {
    interval = (canvas.width - (margin * 2)) / size;
    ClearBoard();
    if (page_now == "InGame") {
        DrawBoard(roundBoardResult);
        highLight(y, x, nowTurn);
    } else if (page_now == "GameResult") {
        DrawResultBoard();
    }
}

function drawCircle(x, y, color) {
    ctx.beginPath();
    if (color == 1){
        ctx.arc(margin + (interval / 2) + (interval * x), margin + (interval / 2) + (interval * y), (interval / 2) - 5, 0, Math.PI * 2);
        ctx.fillStyle = "black"
        ctx.fill();
    }
    else if (color == 2){
        ctx.arc(margin + (interval / 2) + (interval * x), margin + (interval / 2) + (interval * y), (interval / 2) - 5, 0, Math.PI * 2);
        ctx.fillStyle = "white"
        ctx.fill();
        ctx.strokeStyle = "black"
        ctx.stroke();
    }
    else if (color == 0)
        ctx.clearRect(margin + 1 + (interval * x), margin + 1 + (interval * y), interval - 2, interval - 2);
    ctx.closePath();
}

function ClearBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    for (var i = 0; i <= size; i++){
        ctx.moveTo(margin, margin + (interval * i));
        ctx.lineTo(margin + (interval * size), margin + (interval * i));
        ctx.stroke();
    }
    for (var i = 0; i <= size; i++){
        ctx.moveTo(margin + (interval * i), margin);
        ctx.lineTo(margin + (interval * i), margin + (interval * size));
        ctx.stroke();
    }
    ctx.closePath(); 
}

function highLight(x, y, color){
    interval = (canvas.width - (margin * 2)) / size;
    ctx.beginPath();
    if (color == 1){
        ctx.fillStyle = "white"
        ctx.fillRect(margin + (interval * 0.45) + (interval * x), margin + (interval * 0.45) + (interval * y), interval * 0.1, interval * 0.1);
    }
    else if (color == 2){
        ctx.fillStyle = "black"
        ctx.fillRect(margin + (interval * 0.45) + (interval * x), margin + (interval * 0.45) + (interval * y), interval * 0.1, interval * 0.1);
    }
    ctx.closePath();
}

function DrawBoard(array) {
    for (var y = 0; y < size; ++y) {
        for (var x = 0; x < size; ++x) {
            drawCircle(x, y, array[y][x]);
        }
    }
}

function gameStart(data) {
    GoToInGame();
}

function roundStart(data) {
    users = data.players;
    $("#id_title").html("● "+users[0]+"  vs  "+users[1]+" ○").css("text-align","center");
    $("#id_gameMessage_second").html("Round "+round);
}

function recvTurnResult(game_data) {
    roundBoardResult = game_data.data.board;
    DrawBoard(roundBoardResult);

    if (game_data.data.now_turn == game_data.data.black)
        nowTurn = 1;
    else if (game_data.data.now_turn == game_data.data.white)
        nowTurn = 2;
    x = game_data.data.x;
    y = game_data.data.y;
    highLight(y, x, nowTurn) // Interchange x, y temporarily
}

function recvGameResult(game_data) {
    for (var key in game_data.data ) {
        if (game_data.data[key] == "win") {
            alertify.alert(key + " 승리!")
            $("#id_title").html(key+" WIN!").css("text-align","center");
        }
        else if (game_data.data[key] == "draw") {0
            alertify.alert("무승부!")
            $("#id_title").html("DRAW").css("text-align", "center");
        }
    }
    GoToGameResult();
}