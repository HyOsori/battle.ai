var gameResults = [];
var num_list = [];



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
