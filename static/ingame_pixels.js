var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var canvas_width;
var canvas_height;
var width;
var height;
var color_array_old = [];
var color_array = [];
var ruler_array_old = [];
var ruler_array = [];

//  red, orange, yellow, green, blue, purple
var pixel_color = ["#FF0000", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#800080"];
var speed;
var sleep_time;
var pixel_size = 4;
var margin;

var borders = new Queue();
var this_turn_player;
var tiles_get;
var this_turn_color;
var border;

function gameStart() {
    speed
    GoToInGame();
}

function roundStart(player_list) {
    width
    height
    canvas_width
    canvas_height
    margin
    sleep_time = speed / (width * height);

    DrawBoard(color_array_old);
}

function recvTurnResult(data) {
    color_array_old = color_array;
    color_array
    ruler_array_old = ruler_array;
    ruler_array

    this_turn_color
    this_turn_player

    GetIndexNewTiles(ruler_array_old, ruler_array);
	GetBorder(ruler_array_old, this_turn_player);

    var paint_border = setInterval(function() {
		if (!borders.isEmpty()) {
			border = borders.dequeue();
			PaintBorder(ruler_array_old, border, this_turn_color, this_turn_player);
		} else {
			clearInterval(paint_border);
		}
	}, sleep_time);
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

function GetBorder(array_old, this_turn) {
	var x, y;
	for (var i = 0; i < tiles_get.length; i++) {
		x = tiles_get[i][0];
		y = tiles_get[i][1];
		if ((x >= 1 && array_old[y][x - 1] == this_turn) ||
			(y >= 1 && array_old[y - 1][x] == this_turn) ||
			(x <= (width - 2) && array_old[y][x + 1] == this_turn) ||
			(y <= (height - 2) && array_old[y + 1][x] == this_turn)) {
			borders.enqueue([x, y]);
		}
	}
}

function GetIndexNewTiles(array_old, array) {
	tiles_get = [];

	for (var y = 0; y < height; y++) {
		for (var x = 0; x < width; x++) {
			if (array_old[y][x] != array[y][x]) {
				tiles_get.push([x, y]);
			}
		}
	}
}

function PaintPixel(x, y, color) {
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.fillRect(margin + (x * pixel_size), margin + (y * pixel_size), pixel_size, pixel_size);
    ctx.closePath();
}

function DrawBoard(array) {
	for (var y = 0; y < height; y++) {
		for (var x = 0; x < width; x++) {
			PaintPixel(x, y, pixel_color[array[y][x]]);
		}
	}
}

function PaintBorder(array_old, border, color, this_turn) {
	var x = border[0];
	var y = border[1];

	if (x >= 1 && array_old[y][x - 1] == this_turn) {
		PaintPixel(x - 1, y, color);
		array_old[y][x - 1] = 0;
		borders.enqueue([x - 1, y]);
	}
	if (y >= 1 && array_old[y - 1][x] == this_turn) {
		PaintPixel(x, y - 1, color);
		array_old[y - 1][x] = 0
		borders.enqueue([x, y - 1]);
	}
	if (x <= (width - 2) && array_old[y][x + 1] == this_turn) {
		PaintPixel(x + 1, y, color);
		array_old[y][x + 1] = 0;
		borders.enqueue([x + 1, y]);
	}
	if (y <= (height - 2) && array_old[y + 1][x] == this_turn) {
		PaintPixel(x, y + 1, color);
		array_old[y + 1][x] = 0;
		borders.enqueue([x, y + 1]);
	}
}