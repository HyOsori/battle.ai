var gameResults = [];
var loopResult = [];
var roundResult = [];
var loopNum = 0;

function DrawResultBoard(index, loop_num) {
    var nav = document.getElementById('id_gameResults_ul');
    if (loop_num == 0) {
        DrawBoard(gameResults[index]["loop1"]["board"]);
    } else if (loop_num == 1) {
        DrawBoard(gameResults[index]["loop2"]["board"]);
    }
}

function SaveRoundResult(winner){
    $('<li />').bind('click', function(event) {
        var index = 0;
        var nav = document.getElementById('id_gameResults_ul');
        if (event.target.className == 'class_selected') {
            if (loopNum == 0) {
                loopNum = 1;
            } else if (loopNum == 1) {
                loopNum = 0;
            }
            for (index; index < nav.childNodes.length; index++) {
                var child = nav.childNodes[index];
                if (child.className == 'class_selected') {
                    break;
                }
            }
        } else {
            for (var i = 0; i < nav.childNodes.length; i++) {
                var child = nav.childNodes[i];
                if (child.className == 'class_selected') {
                    child.innerHTML = 'Round ' + (i + 1) + ' ' + gameResults[i]["winner"];
                }
                child.className = '';
            }

            event.target.className = 'class_selected';
            loopNum = 0;
            
            for (index; index < nav.childNodes.length; index++) {
                var child = nav.childNodes[index];
                if (child.className == 'class_selected') {
                    break;
                }
            }
            SpreadList(index);
        }

        DrawResultBoard(index, loopNum);
    }).append('Round ', round, ' ', winner).appendTo('#id_gameResults_ul')
}

function SpreadList(index) {
    var nav = document.getElementById("id_gameResults_ul");
    var child = nav.childNodes[index];
    child.className = 'class_selected';

    var player1 = gameResults[index]["loop1"]["score"][0];
    var player2 = gameResults[index]["loop1"]["score"][1];
    var player1_2r = gameResults[index]["loop2"]["score"][0];
    var player2_2r = gameResults[index]["loop2"]["score"][1];

    $("#id_gameResults_ul .class_selected").append('<br>', player1[0], " ", player1[1], " : ", player2[1], " ", player2[0],
        '<br>', player1_2r[0], " ", player1_2r[1], " : ", player2_2r[1], " ", player2_2r[0]);
}

function recvLoopResult(data) {
    var first = data.first;
    var second = data.second;
    var player1 = [];
    var player2 = [];
    var players = [];
    
    player1[0] = first;
    player1[1] = 0;
    players[0] = player1;

    player2[0] = second;
    player2[1] = 0;
    players[1] = player2;
    
    loopResult = [];
    loopResult["board"] = color_array;
    loopResult["score"] = players;

    if (data.round == 0) {
        roundResult["loop1"] = loopResult;
    } else if (data.round == 1) {
        roundResult["loop2"] = loopResult;
    }

    var start_points =  new Array(2);
	start_points[0] = data.start_point_x;
	start_points[1] = data.start_point_y;

    border1 = new Queue();
	border2 = new Queue();

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
    
    if (data.round == 0) {
        DrawBoard(color_array_init);
        console.log(color_array_init);    
    }
    google.charts.setOnLoadCallback(drawRoundChart());
    turn = 0;
    loop++;
    loop_score = [];
    loop_score[0] = ['Turn', 'Player1', 'Player2'];
}

function recvRoundResult(data) {
    roundResult["winner"] = data.winner;
    roundResult["loop1"]["score"][0][1] = data.score[0][0];
    roundResult["loop1"]["score"][1][1] = data.score[0][1];
    roundResult["loop2"]["score"][0][1] = data.score[1][1];
    roundResult["loop2"]["score"][1][1] = data.score[1][0];

    gameResults.push(roundResult);
    SaveRoundResult(roundResult["winner"]);

    roundResult = [];

    round++;
    loop = 0;
    ClearBoard();
}

function recvGameResult(data) {
    var array = [];
    var inner_array = [];
    var winner_index = 0;
    var isDraw = false;
    
    $.each(data, function (key) {
        if (key != "error_code") {
            inner_array.push(key);
            inner_array.push(data.key);
            array.push(inner_array);
            inner_array = [];
        }
    })

    for (var i = 0; i < data.length; ++i) {
        if (array[winner_index][1] == array[i][1]) {
            isDraw = true;
        } else {
            isDraw = false;
            if (array[winner_index][1] < array[i][1]) {
                winner_index = i;
            }
        }
    }

    GoToGameResult();
    round_score = [];
    round_score = [['Round', 'Player1', 'Player2'], [1, 0, 0], [2, 0, 0], [3, 0, 0], [4, 0, 0]];

    if (!isDraw) {
        alertify.alert(array[winner_index][0] + " 승리!");
        $("#id_title").html(array[winner_index][0] + " WIN!");
    } else {
        alertify.alert("무승부!");
        $("#id_title").html("DRAW");
    }
}

$('#id_goToLobby_btn').bind('click',function(){
    round = 1;
    GoToLobby();

    $("#id_gameResults_ul").empty();
    $("#id_dummyclient_ul").empty();

    ClearBoard();
});
