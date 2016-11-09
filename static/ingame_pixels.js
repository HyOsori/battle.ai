google.charts.load('current', {'packages':['corechart']});

var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var users = [];
var round = 1;
var turn = 1;
var loop = 0;
var loop_score = [['Turn', 'Player1', 'Player2']];
var round_score = [['Round', 'Player1', 'Player2']];

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

var this_turn_player;
var this_turn_color;
var border1, border2;

function gameStart(data) {
    users = data.users;
	GoToInGame();
}

function roundStart(data) {

}

function loopStart(data) {
	var start_points =  new Array(2);
	start_points[0] = data.start_point_x;
	start_points[1] = data.start_point_y;
	
	//get PIXELS board size
	width = data.width;
	height = data.height;

	border1 = new Queue();
	border2 = new Queue();

	//save initial color_array
	color_array_init = data.color_array;

	//initialize ruler_array, color_array;
	ruler_array = new Array(height);
	color_array = new Array(height);
	for (var y = 0; y < height; ++y) {
		ruler_array[y] = new Array(width);
		color_array[y] = new Array(width);
		for (var x = 0; x < width; ++x) {
			ruler_array[y][x] = 0
			color_array[y][x] = color_array_init[y][x];
		}
	}
	
	ruler_array[start_points[1][0]][start_points[0][0]] = 1;
	ruler_array[start_points[1][1]][start_points[0][1]] = 2;
	
	border1.enqueue([start_points[0][0], start_points[1][0]]);
	border2.enqueue([start_points[0][1], start_points[1][1]]);
	
	//calculate pixel size
	if ((canvas.width * ratio / width) < (canvas.height * ratio / height)) {
		pixel_size = canvas.width * ratio / width;
	} else {
		pixel_size = canvas.height * ratio / height;
	}

	pixel_size--;

	//calculate margin
	margin_width = (canvas.width - (pixel_size + 1) * width) / 2;
	margin_height = (canvas.height - (pixel_size + 1) * height) / 2;
	
	DrawBoard(color_array_init);
}

function recvTurnResult(data) {
	var score = data.score[loop];
	this_turn_color = data.chosen_color;
	this_turn_player = data.ruler_who;

	RenewArray(this_turn_color, this_turn_player);
	DrawBoard(color_array);
	loop_score.push([turn, score[0], score[1]]);
	google.charts.setOnLoadCallback(drawLoopChart());
	turn++;
}

function PaintPixel(x, y, color) {
    ctx.beginPath();
    ctx.fillStyle = colors[color];
    ctx.fillRect(margin_width + (x * (pixel_size + 1)), margin_height + (y * (pixel_size + 1)), pixel_size, pixel_size);
    ctx.strokeStyle="#FFFFFF";
	ctx.strokeRect(margin_width + (x * (pixel_size + 1)), margin_height + (y * (pixel_size + 1)), (pixel_size + 1), (pixel_size + 1));
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
	RenewRulerArray(color, ruler);
}

function RenewRulerArray(color, ruler) {
	var border, x, y, count;
	var buffer_queue = new Queue();
	var buffer_queue2 = new Queue();
	var i = 0;
	if (ruler == 1) {
		buffer_queue2 = border1;
	} else if (ruler == 2) {
		buffer_queue2 = border2;
	}
	
	while (true) {
		border = buffer_queue2.dequeue();
		count = 0;
		x = border[0];
		y = border[1];
		
		if (x >= 1 && color_array[y][x - 1] == color && ruler_array[y][x - 1] != ruler) {
			buffer_queue2.enqueue([x - 1, y]);
			ruler_array[y][x - 1] = ruler;
			count++;
		} 
		if (y >= 1 && color_array[y - 1][x] == color && ruler_array[y - 1][x] != ruler) {
			buffer_queue2.enqueue([x, y - 1]);
			ruler_array[y - 1][x] = ruler;
			count++;
		}
		if (x <= (width - 2) && color_array[y][x + 1] == color && ruler_array[y][x + 1] != ruler) {
			buffer_queue2.enqueue([x + 1, y]);
			ruler_array[y][x + 1] = ruler;
			count++;
		}
		if (y <= (height - 2) && color_array[y + 1][x] == color && ruler_array[y + 1][x] != ruler) {
			buffer_queue2.enqueue([x, y + 1]);
			ruler_array[y + 1][x] = ruler;
			count++;
		}
		
		if (count < 4) {
			buffer_queue.enqueue([x, y]);
		}

		if (buffer_queue2.isEmpty()) {
			if (ruler == 1) {
				border1 = buffer_queue;
			} else if (ruler == 2) {
				border2 = buffer_queue;
			}
			break;
		}
	}
}

function ClearBoard() {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.beginPath();
}

function drawLoopChart() {
	var data = google.visualization.arrayToDataTable(loop_score);
	var options = {
	  title: 'This Game',
	  hAxis: {title: 'Turn',  titleTextStyle: {color: '#333'}},
	  vAxis: {minValue: 0}
	};
	var chart = new google.visualization.AreaChart(document.getElementById('id_chart1'));
	chart.draw(data, options);
}

function drawRoundChart() {
	var data = google.visualization.arrayToDataTable(round_score);
	var options = {
	  title: 'Total Round',
	  hAxis: {title: 'Round',  titleTextStyle: {color: '#333'}},
	  vAxis: {minValue: 0}
	};
	var chart = new google.visualization.AreaChart(document.getElementById('id_chart2'));
	chart.draw(data, options);
}

function ReadyAfterResize() {
	if ((canvas.width * ratio / width) < (canvas.height * ratio / height)) {
		pixel_size = canvas.width * ratio / width;
	} else {
		pixel_size = canvas.height * ratio / height;
	}

	pixel_size--;

	margin_width = (canvas.width - (pixel_size + 1) * width) / 2;
	margin_height = (canvas.height - (pixel_size + 1) * height) / 2;
	if (page_now == "InGame") {
		DrawBoard(color_array);	
	} else if (page_now == "GameResult") {
		var nav = document.getElementById('id_gameResults_ul');
		var index = 0;
		for(index; index<nav.childNodes.length; index++){
            var child = nav.childNodes[index];
            if (child.className == 'class_selected') {
                break;
            }
        }
		if (index >= nav.childNodes.length) {
			index = 0;
		}
		DrawResultBoard(index);
	}
	
}