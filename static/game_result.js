


function goToLobby(){
    $(".class_lobby").css("display","");
    $(".class_ingame").css("display","none");
    $(".class_gameResult").css("display","none");

    var json = new Object();
    json.msg = "request_user_list";
    var req = JSON.stringify(json);
    ws.send( req );
}

$('#id_goToLobby_btn').bind('click',goToLobby);
