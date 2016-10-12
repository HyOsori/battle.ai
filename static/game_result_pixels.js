function SaveRoundResult(){
    $('<li />').bind('click', function(event) {

    }).append().appendTo('#id_gameResults_ul')
}

function recvRoundResult(data) {
    SaveRoundResult();
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
