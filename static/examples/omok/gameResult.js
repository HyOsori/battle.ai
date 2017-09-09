GameResult.width = -1;
GameResult.height = -1;

GameResult.margin = 10;
GameResult.interval = -1;

GameResult.board = [];

//-------------------------------------------------------------------
GameResult.recvGameResult = function(JSON_data) {
    resizeCanvas(GameResult.canvas);
    
    GameResult.width = GameBoard.width;
    GameResult.height = GameBoard.height;
    GameResult.interval = (GameResult.canvas.width - (GameResult.margin * 2)) / (GameResult.width + 1);
    GameResult.board = GameBoard.board;
    
    GameResult.drawLine();
    GameResult.drawBoard(GameResult.board);
    loadPage("gameResult");
};

GameResult.drawCircle = function(x, y, color) {
    var ctx = GameResult.ctx;
    var margin = GameResult.margin;
    var interval = GameResult.interval;

    ctx.beginPath();
    if (color == 1) {
        ctx.arc(margin + interval * (x + 1), margin + interval * (y + 1), interval * 0.38, 0, Math.PI * 2);
        ctx.fillStyle = "black";
        ctx.fill();
    } else if (color == 2) {
        ctx.arc(margin + interval * (x + 1), margin + interval * (y + 1), interval * 0.38, 0, Math.PI * 2);
        ctx.fillStyle = "white";
        ctx.fill();
    } else if (color == 0) {
        ctx.fillStyle = "#ffcc66";
	    ctx.fillRect(margin + 1 + interval * (x + 1), margin + 1 + interval * (y + 1), interval - 2, interval - 2);
    }
    ctx.closePath();
};

GameResult.drawLine = function() {
    var ctx = GameResult.ctx;
    var margin = GameResult.margin;
    var interval = GameResult.interval;
    var width = GameResult.width;
    var height = GameResult.height;

	ctx.fillStyle="#ffcc66";
	ctx.fillRect(0, 0, GameResult.canvas.width, GameResult.canvas.height);

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

GameResult.drawBoard = function(array) {
    for (var y = 0; y < GameResult.height; ++y) {
        for (var x = 0; x < GameResult.width; ++x) {
            GameResult.drawCircle(x, y, array[y][x]);
        }
    }
};
