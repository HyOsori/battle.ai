gameResults = [];
var num_list = [];

for(var i=0; i<gameResults.length; i++){
    var blackNum = 0;
    var whiteNum = 0;
    for(var j=0; j<8; j++){
        for(var k=0; k<8; k++){
            if (gameResults[i][j][k]==1)
                blackNum++;
            else if (gameResults[i][j][k]==2)
                whiteNum++;
        }
    }
    num_list.push([blackNum,whiteNum]);
}

for(var i=0; i<gameResults.length; i++){
    if (num_list[i][0] > num_list[i][1])
        appendToList(i+1,num_list[i][0],num_list[i][1],"black","white");
    else if (num_list[i][0] < num_list[i][1])
        appendToList(i+1,num_list[i][0],num_list[i][1],"white","black");
    else if (num_list[i][0] == num_list[i][1])
        appendToList(i+1,num_list[i][0],num_list[i][1],"gainsboro","black");
}

function drawBoard(parent){
    var index = 0;
    for(index; index<parent.childNodes.length; index++){
        var child = parent.childNodes[index];
        if (child.className == 'selected')
            break;
    }
    for(var i=0; i<8; i++){
        for(var j=0; j<8; j++){
            drawCircle(j,i,gameResults[index][i][j]);
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
        drawBoard(nav);
    }).append('Round ',round,' ',blackStone,' ',blackNum,' : ',whiteStone,' ',whiteNum).css({"background-color":backgroundColor, "color":fontColor}).appendTo('#id_gameResults_ul')
}

$('#id_goToLobby_btn').bind('click',goToLobby);
