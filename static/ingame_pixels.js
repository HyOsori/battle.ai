var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var users = [];
var round = 1;
var score = [];

var width;
var height;
var color_array_init = [];
var color_array = [];
var ruler_array = [];

//  white, red, orange, yellow, green, blue, purple
var colors = ["#FFFFFF", "#FF0000", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#800080"];
var pixel_size;
var margin_width;
var margin_height;
var ratio = 0.8;

var borders;
var this_turn_player;
var tiles_get;
var this_turn_color;
var border;

function gameStart(data) {
    users = data.users;
	GoToInGame();
}

function roundStart(data) {

}

function loopStart(data) {
	//get PIXELS board size
	width = data.width;
    height = data.height;

	//save initial color_array
	color_array_init = data.color_array;
	color_array = data.color_array;

	//initialize ruler_array
	ruler_array = new Array(height);
	for (var y = 0; y < height; ++y) {
		ruler_array[y] = new Array(width);
		for (var x = 0; x < width; ++x) {
			ruler_array[y][x] = 0;
		}
	}

	//TODO:get starting points and push them in ruler_array
	/*
	for (var i = 0; i < users.length; ++i) {
		borders[i] = new Queue();
		border[i].enqueue();
		ruler_array[][] =;
	}
	*/
	
	//calculate pixel size
	if ((canvas.width * ratio / width) < (canvas.height * ratio / height)) {
		pixel_size = canvas.width * ratio / width;
	} else {
		pixel_size = canvas.height * ratio / height;
	}

	//calculate margin
	margin_width = (canvas.width - pixel_size * width) / 2;
	margin_height = (canvas.height - pixel_size * height) / 2;
	
	DrawBoard(color_array_init);
}

function recvTurnResult(data) {
	this_turn_color = data.chosen_color;
	this_turn_player = data.ruler_who;

	RenewArray(this_turn_color, this_turn_player);
	DrawBoard(color_array);
}	

function PaintPixel(x, y, color) {
    ctx.beginPath();
    ctx.fillStyle = colors[color];
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

function RenewArray(color, ruler) {
	for (var y = 0; y < height; ++y) {
		for (var x = 0; x < width; ++x) {
			if (ruler_array[y][x] == ruler) {
				color_array[y][x] = color;
			}
		}
	}
	RenewRulerArray(borders[ruler], color, ruler);
}

function RenewRulerArray(ruler_queue, color, ruler) {
	var border, x, y, count;
	var buffer_queue = new Queue();
	
	while (true) {
		border = ruler_queue.dequeue();
		count = 0;
		x = border[0];
		y = border[1];
		
		if (x >= 1 && color_array[y][x - 1] == color) {
			ruler_queue.enqueue([x - 1, y]);
			ruler_array[y][x - 1] = ruler;
			count++;
		} 
		if (y >= 1 && color_array[y - 1][x] == color) {
			ruler_queue.enqueue([x, y - 1]);
			ruler_array[y - 1][x] = ruler;
			count++;
		}
		if (x <= (width - 2) && color_array[y][x + 1] == color) {
			ruler_queue.enqueue([x + 1, y]);
			ruler_array[y][x + 1] = ruler;
			count++;
		}
		if (y <= (height - 2) && color_array[y + 1][x] == color) {
			ruler_queue.enqueue([x, y + 1]);
			ruler_array[y + 1][x] = ruler;
			count++;
		}
		
		if (count < 4) {
			buffer_queue.enqueue([x, y]);
		}

		if (ruler_queue.isEmpty()) {
			ruler_queue = buffer_queue;
			break;
		}
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
		DrawResultBoard(0);
	}
	
}