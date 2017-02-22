var roundBoardResult;
var roundResult = [];
var gameResults = [];

function DrawResultBoard(){
    var nav = document.getElementById('id_gameResults_ul');
    var index = 0;
    for(index; index<nav.childNodes.length; index++){
        var child = nav.childNodes[index];
        if (child.className == 'class_selected')
            break;
    }

    for(var i=0; i<8; i++){
        for(var j=0; j<8; j++){
            drawCircle(j,i,gameResults[index]["board"][i][j]);
        }
    }
}

function SaveRoundResult(round, blackNum, whiteNum){
    var whiteStone = $('<img />').attr({
        src:"https://upload.wikimedia.org/wikipedia/en/2/20/Realistic_White_Go_Stone.svg",
        height:"12",
        width:"12"
    })
    var blackStone = $('<img />').attr({
        src:"https://upload.wikimedia.org/wikipedia/en/b/b6/Realistic_Go_Stone.svg",
        height:"12",
        width:"12"
    })
    var background_color;
    var font_color;

    if (blackNum > whiteNum) {
        background_color = "black";
        font_color = "white";
    } else if (blackNum < whiteNum) {
        background_color = "white";
        font_color = "black";
    } else if (blackNum == whiteNum) {
        background_color = "gainsboro";
        font_color = "black";
    }
    
    $('<li />').bind('click', function(event) {
        var nav = document.getElementById('id_gameResults_ul');
        for (var i=0; i<nav.childNodes.length; i++){
            var child = nav.childNodes[i];
            child.className = '';
        }
        if (event.target != this)
            event.target.closest("li").className = 'class_selected';
        else
            event.target.className = 'class_selected';
        DrawResultBoard();
    }).append('Round ',round,' ',blackStone,' ',blackNum,' : ',whiteStone,' ',whiteNum).css({"background-color":background_color, "color":font_color}).appendTo('#id_gameResults_ul')
}

function recvRoundResult(data) {
    var roundScoreResult = data.data;
    roundResult["board"]=roundBoardResult;
    roundResult["score"]=roundScoreResult;
    roundResult["round"]=round;
    gameResults.push(roundResult);
    roundResult=[];
    
    SaveRoundResult(round,roundScoreResult["black_score"],roundScoreResult["white_score"]);
    
    round++;
    
    $("#id_gameMessage_second").html("Round "+round);
    ClearBoard();
}

$('#id_goToLobby_btn').bind('click',function(){
    GoToLobby();
    roundBoardResult=[];
    gameResults=[];
    roundResult=[];
    round=1;

    $("#id_gameResults_ul").empty();
    $("#id_dummyclient_ul").empty();

    var json = new Object();
    json.msg = "request_user_list";
    var req = JSON.stringify(json);
    ws.send( req );

    for(var i=0; i<8; i++){
        for(var j=0; j<8; j++){
            drawCircle(j,i,0);
        }
    }
});
