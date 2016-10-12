var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var margin = 10;
var size_pixel = 2;
//  black, white, red, orange, yellow, green, blue, purple
var pixel_color = ["#000000", "#FFFFFF", "#FF0000", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#800080"];

var tiles_player1 = [];
var tiles_player2 = [];
var tiles_get = [];
var tiles_border = new Queue();
var board_prior = [];
var board_this_turn = [];

function gameStart(user_list) {
    GoToInGame();
}

function recvTurnResult(data) {

}

function recvGameResult(data) {
    for (var key in data.game_data ) {
        if (data.game_data[key] == "win") {
            alertify.alert(key + " 승리!")
            $("#id_title").html(key+" WIN!").css("text-align","center");
        }
        else if (data.game_data[key] == "draw") {
            alertify.alert("무승부!")
            $("#id_title").html("DRAW").css("text-align", "center");
        }
    }
    GoToGameResult();
}

function PaintPixel(x, y, color) {
    ctx.beginPath();
    ctx.fillStyle = color
    ctx.fillRect(margin + (x * size_pixel), margin + (y * size_pixel), size_pixel, size_pixel);
    ctx.closePath();
}

function GetIndexNewTiles () {

}