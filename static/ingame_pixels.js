var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var users = [];
var round = 1;
var score = [];

var width;
var height;
var color_array_old = [];
var color_array = [];
var ruler_array_old = [];
var ruler_array = [];

//  white, red, orange, yellow, green, blue, purple
var pixel_color = ["#FFFFFF", "#FF0000", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#800080"];
var speed;
var sleep_time;
var loop_num = 1;
var pixel_size = 2;
var margin_width;
var margin_height;

var borders = new Queue();
var this_turn_player;
var tiles_get;
var this_turn_color;
var border;


function gameStart(data) {
    loop_num = 1;
	speed = data.data.speed * 1000;
    users = data.data.users;
	GoToInGame();
}

function roundStart(data) {

}

function loopStart(data) {
	width = data.width;
    height = data.height;
	color_array = data.color_array;
	ruler_array = data.ruler_array;
	
	if ((canvas.width * 0.8 / width) < (canvas.height * 0.8 / height)) {
		pixel_size = canvas.width * 0.8 / width;	
	} else {
		pixel_size = canvas.height * 0.8 / height;
	}
	
	margin_width = (canvas.width - pixel_size * width) / 2;
	margin_height = (canvas.height - pixel_size * height) / 2;

	sleep_time = speed / (width * height);
	while ((speed * loop_num) < (4 * width * height)) { // minimum delay of setInterval : 4
		loop_num++;
	}


	DrawBoard(color_array);
}

function recvTurnResult(game_data) {
	color_array_old = color_array;
    color_array = game_data.data.color_array;
    ruler_array_old = ruler_array;
    ruler_array = game_data.data.ruler_array;

    this_turn_color = game_data.data.chosen_color;
    this_turn_player = game_data.data.ruler_who;

    GetIndexNewTiles(ruler_array_old, ruler_array);
	GetBorder(ruler_array_old, this_turn_player);

    var paint_border = setInterval(function() {
		for (var i = 0; i < loop_num; ++i) {
			if (!borders.isEmpty()) {
				border = borders.dequeue();
				PaintBorder(ruler_array_old, border, this_turn_color, this_turn_player);
			} else {
				clearInterval(paint_border);
			}
		}
	}, sleep_time);
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
    ctx.fillStyle = pixel_color[color];
    ctx.fillRect(margin_width + (x * pixel_size), margin_height + (y * pixel_size), pixel_size, pixel_size);
    ctx.closePath();
}

function DrawBoard(array) {
	for (var y = 0; y < height; y++) {
		for (var x = 0; x < width; x++) {
			PaintPixel(x, y, array[y][x]);
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

function ClearBoard() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.beginPath();
}

function ReadyAfterResize() {
	margin_width = (canvas.width - pixel_size * width) / 2;
	margin_height = (canvas.height - pixel_size * height) / 2;
	if (page_now == "InGame") {
		DrawBoard(color_array);	
	} else if (page_now == "GameResult") {
		DrawResultBoard();
	}
	
}