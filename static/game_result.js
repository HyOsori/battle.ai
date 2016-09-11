var roundBoardResult;
var roundResult = [];
var gameResults = [];


function drawBoard(){
    var nav = document.getElementById('id_gameResults_ul');
    var index = 0;
    for(index; index<nav.childNodes.length; index++){
        var child = nav.childNodes[index];
        if (child.className == 'selected')
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
            event.target.closest("li").className = 'selected';
        else
            event.target.className = 'selected';
        drawBoard();
    }).append('Round ',round,' ',blackStone,' ',blackNum,' : ',whiteStone,' ',whiteNum).css({"background-color":backgroundColor, "color":fontColor}).appendTo('#id_gameResults_ul')
}

$('#id_goToLobby_btn').bind('click',function(){
    goToLobby();
    roundBoardResult=[];
    gameResults=[];
    roundResult=[];
    round=1;
    $("#id_gameResults_ul").empty();

    for(var i=0; i<8; i++){
        for(var j=0; j<8; j++){
            drawCircle(j,i,0);
        }
    }
});
