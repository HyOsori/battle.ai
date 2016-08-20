var MIN_MATCH_USER_CNT = 2;
var MAX_MATCH_USER_CNT = 2;

var list = [];
var messageContainer = document.getElementById('id_messages');
var userList = document.getElementById('id_list_ul');

function goToLobby(){
    $("#id_board_canvas").css("display","none");
    $("#id_gameResults_ul").css("display","none");
    $("#id_goToLobby_btn").css("display","none");
    $("#id_conn_btn").css("display","");
    $("#id_conn_id").css("display","");
    $("#id_list_ul").css("display","");
    $("#id_match_btn").css("display","");
    $("#id_messages").css("display","");

    $("#id_gameMessage").html("Othello");

    $("#id_list_ul").empty();

    var json = new Object();
    json.msg = "request_user_list";
    var req = JSON.stringify(json);
    ws.send( req );
}

function goToInGame(){
    $("#id_board_canvas").css("display","");
    $("#id_gameResults_ul").css("display","none");
    $("#id_goToLobby_btn").css("display","");
    $("#id_conn_btn").css("display","none");
    $("#id_conn_id").css("display","none");
    $("#id_list_ul").css("display","none");
    $("#id_match_btn").css("display","none");
    $("#id_messages").css("display","none");

    for(var i=0; i<8; i++){
        for(var j=0; j<8; j++){
            drawCircle(j,i,0);
        }
    }
}

function goToGameResult(){
    $("#id_board_canvas").css("display","");
    $("#id_gameResults_ul").css("display","");
    $("#id_goToLobby_btn").css("display","");
    $("#id_conn_btn").css("display","none");
    $("#id_conn_id").css("display","none");
    $("#id_list_ul").css("display","none");
    $("#id_match_btn").css("display","none");
    $("#id_messages").css("display","none");

    for(var i=0; i<8; i++){
        for(var j=0; j<8; j++){
            drawCircle(j,i,0);
        }
    }
}

function checkSelected(){
    var count = 0;
    for(var i=0; i<userList.childNodes.length; i++){
        var child = userList.childNodes[i];
        if (child.className == 'class_selected')
            count++;
    }
    return count;
}

function clickHandler(event) {
    var button = document.getElementById('id_match_btn');
    button.disabled='true';
    if (event.target.className == 'class_selected'){
        event.target.className = '';
    }
    else if (checkSelected()<MAX_MATCH_USER_CNT){
            event.target.className = 'class_selected';
    }
    if (checkSelected()>=MIN_MATCH_USER_CNT) {
        button.removeAttribute('disabled');
    }
}

//Size of elements
$("#id_container").css({"width":window.innerHeight*0.95*1.25,"height":window.innerHeight*0.95});
$("#id_gameMessage").css({"width":window.innerHeight*0.95*1.25*0.8,"height":window.innerHeight*0.95*0.1});
$("#id_list_ul").css({"width":window.innerHeight*0.95*1.25*0.2,"height":window.innerHeight*0.95*0.8});
$("#id_board_canvas").attr({"width":window.innerHeight*0.95*0.8,"height":window.innerHeight*0.95*0.8});
$("#id_gameResults_ul").css({"width":window.innerHeight*0.95*1.25*0.25,"height":window.innerHeight*0.95*0.79});
$("#id_messages").css({"width":window.innerHeight*0.95*1.25*0.6,"height":window.innerHeight*0.95*0.25});
$("#id_goToLobby_btn").css({"width":window.innerHeight*0.95*1.25*0.25,"height":window.innerHeight*0.95*0.05});

function getSelected(){
    var selectedUser = [];
    for (var i=0; i<userList.childNodes.length; i++){
        var child = userList.childNodes[i];
        if (child.className == 'class_selected'){
            selectedUser.push(child.innerText);
        }
    }
    var json = new Object();
    json.msg = "request_match";
    json.users = selectedUser;
    var req = JSON.stringify(json);
    ws.send( req );
}

if ("WebSocket" in window) {
    var btnConn = document.getElementById('id_conn_btn');
    var message = "";

    messageContainer.innerHTML = "WebSocket is supported by your Browser!";
    var ws = new WebSocket("ws://localhost:9000/websocket");
    goToLobby();
    ws.onmessage = function (evt) {
        var received_msg = evt.data;
        message += ">> " + received_msg + "<br>";
        messageContainer.innerHTML = message;

        var data = jQuery.parseJSON(received_msg);

        if (data.msg == "response_user_list") {
            alertify.alert("승리 팝업");
            alertify.whitewin("흰돌 승리!", 2000);
            alertify.blackwin("검은돌 승리!", 2000);
            alertify.draw("비겼다!", 2000);
            $.each(data.users, function (key) {
                var text = data.users[key];
                for (var i = 0; i < userList.childNodes.length; i++) {
                    var child = userList.childNodes[i];
                    if (text == child.innerText)
                        return;
                }
                if (text.length) {
                    $('<li />', {html: text}).bind('click', clickHandler).appendTo('#id_list_ul')
                    list.push(text);
                }
            })
        }
        else if (data.msg == "notice_user_added") {
            var text = data.user;
            for (var i = 0; i < userList.childNodes.length; i++) {
                var child = userList.childNodes[i];
                if (text == child.innerText)
                    return;
            }
            if (text.length) {
                $('<li />', {html: text}).bind('click', clickHandler).appendTo('#id_list_ul')
                list.push(text);
            }
        }

        else if (data.msg == "notice_user_removed") {
            var button = document.getElementById('id_match_btn');
            var text = data.user;
            for (var i = 0; i < userList.childNodes.length; i++) {
                var child = userList.childNodes[i];
                if (text == child.innerText) {
                    child.remove();
                    list.splice((i - 1), 1);

                    if (checkSelected()<MIN_MATCH_USER_CNT)
                        button.disabled='true';
                }
            }
        }
        else if (data.msg == "response_match") {
            gameStart(data.users);
            goToInGame();
            alertify.success("게임 시작!", 2000);
        }
        else if (data.msg == "game_data") {
            recvGameMsg(data);

            // setTimeout(function(){
            //     $(".class_lobby").css("display","none");
            //     $(".class_ingame").css("display","none");
            //     $(".class_gameResult").css("display","");
            //     $("#id_board_canvas").css("display","");
            // },2000);
        }
        else if (data.msg == "game_result") {
            recvGameResult(data);
        }
    }
    $('#id_match_btn').bind('click',getSelected);

    <!-- connect websocket button handler -->
    btnConn.addEventListener('click', function(){
        var json = new Object();
        json.msg = "request_user_list";
        var req = JSON.stringify(json);
        ws.send( req );
    });

    ws.onclose = function() {
        message = "";
        messageContainer.innerHTML = "Connection is closed...";
    }
}
else
{
    messageContainer.innerHTML = "WebSocket NOT supported by your Browser!";
}
