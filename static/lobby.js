var MIN_MATCH_USER_CNT = 2;
var MAX_MATCH_USER_CNT = 2;

var list = [];
var messageContainer = document.getElementById('id_messages');
var userList = document.getElementById('id_list_ul');
var setSpeed = document.getElementById('id_setSpeed');


function goToLobby(){
    $("#id_canvasContainer").css("display","none");
    $("#id_gameResults_ul").css("display","none");
    $("#id_btnContainer").css("display","");
    $("#id_goToLobby_btn").css("display","none");
    $("#id_conn_btn").css("display","");
    $("#id_list_ul").css("display","");
    $("#id_match_btn").css("display","");
    $("#id_messages").css("display","");
    $("#id_gameMessage_second").css("display","none");
    $("#id_log").css("display","");
    $("#id_dummyMatch_btn").css("display","");
    $("#id_chart").css("display","none");
    $("#id_setSpeed").css("display","");

    $("#id_title").html("Othello").css("text-align","left");
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


function getSelected(){
    var selectedUser = [];
    var speed = setSpeed.value;
    var data = new Object();
    for (var i=0; i<userList.childNodes.length; i++){
        var child = userList.childNodes[i];
        if (child.className == 'class_selected'){
            selectedUser.push(child.innerText);
        }
    }

    data.users = selectedUser;
    data.speed = speed;
    
    var json = new Object();
    json.msg = "request_match";
    json.data = data;
    var req = JSON.stringify(json);
    ws.send( req );
}

if ("WebSocket" in window) {
    var btnConn = document.getElementById('id_conn_btn');
    var message = "";

    messageContainer.innerHTML = "WebSocket is supported by your Browser!";
    var ws = new WebSocket("ws://localhost:9000/websocket");
    goToLobby();
    ws.onopen = function (evt) {
        
    };
    ws.onmessage = function (evt) {
        var received_msg = evt.data;
        message += ">> " + received_msg + "<br>";
        messageContainer.innerHTML = message;

        var data = jQuery.parseJSON(received_msg);

        if (data.msg == "response_user_list") {
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
            if (data.data.error == 0) {
                gameStart(data.data.users);
                goToInGame();
                alertify.success("게임 시작!", 2000);
            }
            else {
                alertify.alert("매칭 실패!");
            }
        }
        else if (data.msg == "game_data") {
            recvGameMsg(data);

            if (data.msg_type == "notify_on_turn") {
                roundBoardResult = data.game_data.board;
                var nowTurn;
                if (data.game_data.now_turn == data.game_data.black)
                    nowTurn = 1;
                else if (data.game_data.now_turn == data.game_data.white)
                    nowTurn = 2;
                highLight(data.game_data.y, data.game_data.x, nowTurn) // Interchange x, y temporarily
            }
            else if (data.msg_type == "notify_finish") { // A round is ended
                SaveRoundResult(data);
                $("#id_gameMessage_second").html("Round "+round);
                ClearBoard();
            }
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
