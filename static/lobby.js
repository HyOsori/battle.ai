var MIN_MATCH_USER_CNT = 2;
var MAX_MATCH_USER_CNT = 2;
var Title = "Othello";

var list = [];
var page_now = "Lobby";

var messageContainer = document.getElementById('id_messages');
var userList = document.getElementById('id_list_ul');
var setSpeed = document.getElementById('id_setSpeed');

$(window).resize(ResizeCanvas);

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

if ("WebSocket" in window) {

    var btnConn = document.getElementById('id_conn_btn');
    var message = "";

    messageContainer.innerHTML = "WebSocket is supported by your Browser!";
    var ws = new WebSocket("ws://localhost:9000/websocket");

    GoToLobby();

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
                gameStart(data);
                alertify.success("게임 시작!", 2000);
            }
            else {
                alertify.alert("매칭 실패!");
            }
        }

        else if (data.msg == "game_data") {
            if (data.msg_type == "notify_on_turn") {
                recvTurnResult(data);
            }
            else if (data.msg_type == "notify_finish") {
                recvRoundResult(data);
            }
            else if (data.msg_type == "round_result") {
                
            }
        }

        else if (data.msg == "game_handler") {
            if (data.msg_type == "ready") {
                if (data.data.response = "OK") {
                    roundStart(data.data);
                } else {
                    alertify.alert("매칭 실패!");
                    GoToLobby();
                }
            } else if (data.msg_type == "game_result") {
                recvGameResult(data);
            }
        }
    }

    $('#id_match_btn').bind('click',function() {
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
    });

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



function GoToLobby() {
    $(".class_inGame").css("display","none");
    $(".class_gameResult").css("display","none");
    $(".class_lobby").css("display","");

    $("#id_title").html(Title).css("text-align","left");
    page_now = "Lobby";
}

function GoToInGame() {
    $(".class_lobby").css("display","none");
    $(".class_gameResult").css("display","none");
    $(".class_inGame").css("display","");
    
    page_now = "InGame";
    ResizeCanvas();
}

function GoToGameResult() {
    $(".class_lobby").css("display","none");
    $(".class_inGame").css("display","none");
    $(".class_gameResult").css("display","");
    
    page_now = "GameResult";
    ResizeCanvas();
}

function ResizeCanvas() {
    canvas_size = $("#id_side").css('height');
    $("#id_board_canvas").attr({"width": canvas_size, "height": canvas_size});
    ReadyAfterResize();
}