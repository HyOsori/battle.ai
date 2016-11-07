var gameResults = [];

function DrawResultBoard(index) {
    var nav = document.getElementById('id_gameResults_ul');
    var index = 0;

    DrawBoard(gameResults[index]["round1"]["board"]);
}

function SaveRoundResult(winner){
    $('<li />').bind('click', function(event) {
        var nav = document.getElementById('id_gameResults_ul');
        var index = 0;
        for (var i=0; i<nav.childNodes.length; i++){
            var child = nav.childNodes[i];
            if (child.className == 'class_selected') {
                child.innerHTML = 'Round ' + (i + 1) + ' ' + gameResults[i]["winner"];
            }
            child.className = '';
        }
        
        event.target.className = 'class_selected';
        
        for(index; index<nav.childNodes.length; index++){
            var child = nav.childNodes[index];
            if (child.className == 'class_selected') {
                break;
            }
        }

        var player1 = gameResults[index]["round1"]["player"]["player1"];
        var player2 = gameResults[index]["round1"]["player"]["player2"];
        var player1_2r = gameResults[index]["round2"]["player"]["player1"];
        var player2_2r = gameResults[index]["round2"]["player"]["player2"];
        $(this).append('<br>', player1[0], " ", player1[1], " : ", player2[1], " ", player2[0],
                        '<br>', player1[0], " ", player1[1], " : ", player2[1], " ", player2[0]);
        DrawResultBoard(index);
    }).append('Round ', round, ' ', winner).appendTo('#id_gameResults_ul')
}

function recvRoundResult(data) {
    var roundResult = [];
    var players = [];
    var roundData = [];
    //save winner
    roundResult["winner"] = users[data.win - 1];
    console.log(users[data.win - 1]);
    console.log(users);
    console.log(data.win);
    
    //save round1
    players["player1"] = [users[0], data.ruler1_score];
    players["player2"] = [users[1], data.ruler2_score];
    roundData["player"] = players;
    roundData["board"] = color_array;
    roundResult["round1"] = roundData;

    //save round2
    players["player1"] = [users[1], data.ruler2_score];
    players["player2"] = [users[0], data.ruler1_score];
    roundData["player"] = players;
    roundData["board"] = color_array;
    roundResult["round2"] = roundData;
    
    gameResults.push(roundResult);

    SaveRoundResult(roundResult["winner"]);
    round++;
    ClearBoard();
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

$('#id_goToLobby_btn').bind('click',function(){
    round = 1;
    GoToLobby();

    $("#id_gameResults_ul").empty();

    var json = new Object();
    json.msg = "request_user_list";
    var req = JSON.stringify(json);
    ws.send( req );

    ClearBoard();
});
