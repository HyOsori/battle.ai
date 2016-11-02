var gameResults = [];

function SaveRoundResult(winner){
    $('<li />').bind('click', function(event) {
        var nav = document.getElementById('id_gameResults_ul');
        for (var i=0; i<nav.childNodes.length; i++){
            var child = nav.childNodes[i];
            child.className = '';
        }
        event.target.className = 'class_selected';
        DrawBoard(gameResults[i]["round1"]["board"]);
    }).append('Round ', round, ' ', winner).appendTo('#id_gameResults_ul')
}

function recvRoundResult(data) {
    var roundResult = [];
    var players = [];
    var roundData = [];
    //save winner
    //roundResult["winner"] = data.winner;
    
    //save round1
    //players["data.player1_name"] = data.score_player1_round1;
    //players["data.player2_name"] = data.score_player2_round1;
    //roundData["player"] = players;
    //roundData["board"] = data.board_round1;
    //roundResult["round1"] = roundData;

    //save round2
    //players["data.player1_name"] = data.score_player1_round2;
    //players["data.player2_name"] = data.score_player2_round2;
    //roundData["player"] = players;
    //roundData["board"] = data.board_round2;
    //roundResult["round2"] = roundData;
    
    gameResults.push(roundResult);

    SaveRoundResult(roundResult["winner"]);
    round++;
    ClearBoard();
}

$('#id_goToLobby_btn').bind('click',function(){
    GoToLobby();

    $("#id_gameResults_ul").empty();

    var json = new Object();
    json.msg = "request_user_list";
    var req = JSON.stringify(json);
    ws.send( req );

    ClearBoard();
});
