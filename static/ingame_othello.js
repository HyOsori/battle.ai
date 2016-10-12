var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var margin = 10;
var size = 8;
var interval = (canvas.width - (margin * 2)) / size;

var round = 1;
var canvas_size = $("#id_side").css('height');
var users;



function ReadyNewRound() {
    ClearBoard();
    
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
    for (var i = 0; i < size; i++) {
        for (var j = 0; j < size; j++) {
            drawCircle(j, i, 0);
        }
    }
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

function gameStart(user_list) {
    users = user_list;
    $("#id_title").html("● "+users[0]+"  vs  "+users[1]+" ○").css("text-align","center");
    $("#id_gameMessage_second").html("Round "+round);
    GoToInGame();
}

function recvTurnResult(data) {
    var y = 0;
    $.each(data.game_data.board, function(){
        for (var x = 0; x < size; x++) {
            drawCircle(x, y, this[x]);
        }
        y++;
    })
    
    roundBoardResult = data.game_data.board;
    var nowTurn;
    if (data.game_data.now_turn == data.game_data.black)
        nowTurn = 1;
    else if (data.game_data.now_turn == data.game_data.white)
        nowTurn = 2;
    highLight(data.game_data.y, data.game_data.x, nowTurn) // Interchange x, y temporarily
}

function recvGameResult(data) {
    for (var key in data.game_data ) {
        if (data.game_data[key] == "win") {
            alertify.alert(key + " 승리!")
            $("#id_title").html(key+" WIN!").css("text-align","center");
        }
        else if (data.game_data[key] == "draw") {0
            alertify.alert("무승부!")
            $("#id_title").html("DRAW").css("text-align", "center");
        }
    }
    GoToGameResult();
}