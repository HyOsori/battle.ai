var GameBoard = new Object();

//load elements-----------------------------------------------------
GameBoard.canvas = document.getElementById("id_gameBoard_canvas");
GameBoard.ctx = GameBoard.canvas.getContext("2d");

GameBoard.canvas_text_size = 15;
GameBoard.canvas_text_interval = 1.3;

GameBoard.is_turn_end = true;

GameBoard.turn = 0;

GameBoard.data_init;
GameBoard.data_turns = new Queue();

//basic functions for gameBoard------------------------------------------
GameBoard.startGame = function(JSON_data) {
    if (setting.use_animation) {
        GameBoard.saveInitData(JSON_data);
    } else {
        GameBoard.getReady(JSON_data);
    }
};

GameBoard.saveInitData = function(JSON_data) {
    GameBoard.data_init = JSON_data;
};

GameBoard.getReady = function(JSON_data) {
    GameBoard.turn = 0;
    resizeCanvas(GameBoard.canvas);
};

GameBoard.recvTurnResult = function(JSON_data) {
    if (setting.use_animation) {
        GameBoard.saveTurnData(JSON_data);
    } else {
        GameBoard.drawTurnResult(JSON_data);
    }
};

GameBoard.saveTurnData = function(JSON_data) {
    GameBoard.data_turns.enqueue(JSON_data);
};

GameBoard.drawTurnResult = function(JSON_data) {
    ++GameBoard.turn;

    drawText(GameBoard.canvas, JSONtoString(JSON_data.data), GameBoard.canvas_text_size, 
             -1, GameBoard.turn * GameBoard.canvas_text_size * GameBoard.canvas_text_interval);
};

GameBoard.endGame = function(JSON_data) {
    if (setting.use_animation) {
        loadPage("gameBoard");
        GameBoard.getReady(GameBoard.data_init);
        
        var drawing = setInterval(function() {
            if (GameBoard.data_turns.isEmpty()) {
                clearInterval(drawing);
                setTimeout("loadPage('lobby')", 2000);
                return;
            }

            if (GameBoard.is_turn_end) {
                GameBoard.drawTurnResult(GameBoard.data_turns.dequeue());
            }
        }, 0);

    } else {
        setTimeout("loadPage('lobby')", 2000);
    }
};