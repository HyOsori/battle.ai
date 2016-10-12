var roundBoardResult;
var roundResult = [];
var gameResults = [];

function goToGameResult(){
    $("#id_canvasContainer").css("display","");
    $("#id_gameResults_ul").css("display","");
    $("#id_btnContainer").css("display","");
    $("#id_goToLobby_btn").css("display","");
    $("#id_conn_btn").css("display","none");
    $("#id_list_ul").css("display","none");
    $("#id_match_btn").css("display","none");
    $("#id_messages").css("display","none");
    $("#id_gameMessage_second").css("display","none");
    $("#id_log").css("display","none");
    $("#id_dummyMatch_btn").css("display","none");
    $("#id_chart").css("display","none");
    $("#id_setSpeed").css("display","none");
    
    ResizeCanvas();
}

function drawBoard(){
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

function appendToList(round,blackNum,whiteNum,backgroundColor,fontColor){
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
    $('<li />').bind('click',function(event){
        var nav = document.getElementById('id_gameResults_ul');
        for (var i=0; i<nav.childNodes.length; i++){
            var child = nav.childNodes[i];
            child.className = '';
        }
        if (event.target != this)
            event.target.closest("li").className = 'class_selected';
        else
            event.target.className = 'class_selected';
        drawBoard();
    }).append('Round ',round,' ',blackStone,' ',blackNum,' : ',whiteStone,' ',whiteNum).css({"background-color":backgroundColor, "color":fontColor}).appendTo('#id_gameResults_ul')
}

function SaveRoundResult(data) {
    var roundScoreResult = data.game_data;
    roundResult["board"]=roundBoardResult;
    roundResult["score"]=roundScoreResult;
    roundResult["round"]=round;
    gameResults.push(roundResult);
    roundResult=[];
    
    if(roundScoreResult["black_score"] > roundScoreResult["white_score"])
        appendToList(round,roundScoreResult["black_score"],roundScoreResult["white_score"],"black","white");
    else if(roundScoreResult["black_score"] < roundScoreResult["white_score"])
        appendToList(round,roundScoreResult["black_score"],roundScoreResult["white_score"],"white","black");
    if(roundScoreResult["black_score"] == roundScoreResult["white_score"])
        appendToList(round,roundScoreResult["black_score"],roundScoreResult["white_score"],"gainsboro","black");
    
    round++;
}

$('#id_goToLobby_btn').bind('click',function(){
    goToLobby();
    roundBoardResult=[];
    gameResults=[];
    roundResult=[];
    round=1;

    $("#id_gameResults_ul").empty();

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
