GameBoard.width = -1;
GameBoard.height = -1;

GameBoard.margin = 10;
GameBoard.interval = -1;

GameBoard.players = [];
GameBoard.board = [];
//================================================================================
GameBoard.getReady = function(JSON_data) {
    resizeCanvas(GameBoard.canvas);
    var game_data = JSON_data.data;
    for (var key in game_data) {
        var player = [];
        player.push(key);
        player.push(game_data[key]["color"]);
        GameBoard.players.push(player);

        GameBoard.width = game_data[key]["width"];
        GameBoard.height = game_data[key]["height"];
    }

    GameBoard.turn = 0;
    GameBoard.interval = (GameBoard.canvas.width - (GameBoard.margin * 2)) / (GameBoard.width + 1);
    GameBoard.drawLine();
};

GameBoard.drawTurnResult = function(JSON_data) {
    var game_data = JSON_data.data;
    
    ++GameBoard.turn;
    GameBoard.board = game_data["board"];
    GameBoard.drawBoard(GameBoard.board);
};

GameBoard.endGame = function(JSON_data) {
    resizeCanvas(GameBoard.canvas);

    GameBoard.width = GameBoard.width;
    GameBoard.height = GameBoard.height;
    GameBoard.interval = (GameBoard.canvas.width - (GameBoard.margin * 2)) / (GameBoard.width + 1);
    GameBoard.board = GameBoard.board;

    GameBoard.drawLine();
    GameBoard.drawBoard(GameBoard.board);
};

GameBoard.drawCircle = function(x, y, color) {
    var ctx = GameBoard.ctx;
    var margin = GameBoard.margin;
    var interval = GameBoard.interval;

    ctx.beginPath();
    if (color == 1){
        ctx.arc(margin + interval * (x + 1), margin + interval * (y + 1), interval * 0.38, 0, Math.PI * 2);
        ctx.fillStyle = "black";
        ctx.fill();
    } else if (color == 2){
        ctx.arc(margin + interval * (x + 1), margin + interval * (y + 1), interval * 0.38, 0, Math.PI * 2);
        ctx.fillStyle = "white";
        ctx.fill();
    } else if (color == 0) {
        ctx.fillStyle="#ffcc66";
	    ctx.fillRect(margin + 1 + interval * (x + 1), margin + 1 + interval * (y + 1), interval - 2, interval - 2);
    }
    ctx.closePath();
};

GameBoard.drawLine = function() {
    var ctx = GameBoard.ctx;
    var margin = GameBoard.margin;
    var interval = GameBoard.interval;
    var width = GameBoard.width;
    var height = GameBoard.height;

	ctx.fillStyle="#ffcc66";
	ctx.fillRect(0, 0, GameBoard.canvas.width, GameBoard.canvas.height);

	ctx.strokeStyle="#333300";
	ctx.fillStyle="#333300";
    
    ctx.beginPath();
    for (var i = 0; i < (height + 2); ++i){
        ctx.moveTo(margin, margin + (interval * i));
        ctx.lineTo(margin + (interval * (width + 1)), margin + (interval * i));
        ctx.stroke();
    }
    for (var i = 0; i <= (width + 2); ++i){
        ctx.moveTo(margin + (interval * i), margin);
        ctx.lineTo(margin + (interval * i), margin + (interval * (height + 1)));
        ctx.stroke();
    }
    ctx.closePath();
};

GameBoard.drawBoard = function(array) {
    for (var y = 0; y < GameBoard.height; ++y) {
        for (var x = 0; x < GameBoard.width; ++x) {
            GameBoard.drawCircle(x, y, array[y][x]);
        }
    }
};
