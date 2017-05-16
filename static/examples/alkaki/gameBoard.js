GameBoard.size_num = 18;
GameBoard.blank = 3;

GameBoard.board_size = -1;
GameBoard.ratio = -1;
GameBoard.interval = -1;

GameBoard.egg_radius = -1;
GameBoard.egg_count = []; //[black_egg_cnt, white_egg_cnt]

GameBoard.board = []; //[black_egg_arr, white_egg_arr]

//-----------------------------------------------------------------------------------------------------------
GameBoard.getReady = function(JSON_data) {
    var game_data = JSON_data.data;
    var player_color = -1;
    var x, y;

    for (key in game_data) {
        player_color = game_data[key].color;
        GameBoard.board_size = game_data[key].board_size;
        GameBoard.egg_radius = game_data[key].radius;
        GameBoard.egg_count[player_color] = game_data[key].count;
        GameBoard.board[player_color] = game_data[key].player_pos;
    }

    GameBoard.ratio = GameBoard.canvas.height / GameBoard.board_size;
    GameBoard.interval = (GameBoard.board_size - GameBoard.blank * 2) / GameBoard.size_num;
    
    GameBoard.drawLine();

    for (var color = 0; color < GameBoard.board.length; ++color) {
        for (var i = 0; i < GameBoard.board[color].length; ++i) {
            x = GameBoard.board[color][i][0];
            y = GameBoard.board[color][i][1];
            GameBoard.drawEgg(x, y, color);
        }
    }
    
};

GameBoard.drawTurnResult = function(JSON_data) {
    
};

GameBoard.drawLine = function() {
    var ctx = GameBoard.ctx;
    var interval = GameBoard.interval * GameBoard.ratio;
    var blank = GameBoard.blank * GameBoard.ratio;
    var circle_radius = 3;

    ctx.fillStyle="#ffcc66";
	ctx.fillRect(0, 0, GameBoard.canvas.width, GameBoard.canvas.height);

    // board draw line
	ctx.strokeStyle="#333300";
	ctx.fillStyle="#333300";

	for (var i = 0; i < GameBoard.size_num + 1; ++i) {
		// horizontal line draw
		ctx.beginPath();
		ctx.moveTo(blank + i * interval, blank);
		ctx.lineTo(blank + i * interval, GameBoard.canvas.width - blank);
		ctx.stroke();

		// vertical line draw
		ctx.beginPath();
		ctx.moveTo(blank, blank + i * interval);
		ctx.lineTo(GameBoard.canvas.height - blank, blank + i * interval);
		ctx.stroke();
	}

	// board draw point
	for (i = 0; i < 3; i++) {
		for (var j = 0; j < 3; j++) {
			// board circle draw
			ctx.beginPath();
			ctx.arc(blank + 3 * interval + i * 6 * interval, blank + 3 * interval + j * 6 * interval, circle_radius, 0, 2 * Math.PI);
			ctx.fill();
			ctx.stroke();
		}
	}
};

GameBoard.drawEgg = function(x_rate, y_rate, color) {
    var ctx = GameBoard.ctx;
    var x = x_rate * GameBoard.ratio;
    var y = y_rate * GameBoard.ratio;
    var radius = GameBoard.egg_radius * GameBoard.ratio;

    ctx.beginPath();
    if (color == 0) {
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = "black";
        ctx.fill();
    } else if (color == 1){
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = "white";
        ctx.fill();
    }
    ctx.closePath();
};
