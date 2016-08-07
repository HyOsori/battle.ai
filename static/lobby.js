var MIN_MATCH_USER_CNT = 2;
var MAX_MATCH_USER_CNT = 4;

var list = [];
var messageContainer = document.getElementById('id_messages');

$(".class_lobby").css("display","");
$(".class_ingame").css("display","none");
$(".class_gameResult").css("display","none");

function checkSelected(){
    var count = 0;
    var nav = document.getElementById('id_list_ul');
    for(var i=0; i<nav.childNodes.length; i++){
        var child = nav.childNodes[i];
        if (child.className == 'class_selected')
            count++;
    }
    return count;
}

function clickHandler(event) {
    var nav = document.getElementById('id_list_ul');
    var button = document.getElementById('id_match_btn');
    button.disabled='true';

    if (event.target.className == 'class_selected'){
        event.target.className = '';
    }
    else {
        if (checkSelected()<MAX_MATCH_USER_CNT){
            event.target.className = 'class_selected';
        }
    }

    if (checkSelected()>=MIN_MATCH_USER_CNT) {
        button.removeAttribute('disabled');
    }
}

function getSelected(){
    var nav = document.getElementById('id_list_ul');
    var selectedUser = [];
    for (var i=0; i<nav.childNodes.length; i++){
        var child = nav.childNodes[i];
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
    var textID = document.getElementById('id_conn_id');
    var message = "";

    messageContainer.innerHTML = "WebSocket is supported by your Browser!";
    var ws = new WebSocket("ws://localhost:8888/websocket");
    ws.onmessage = function (evt) {
        var received_msg = evt.data;
        message += ">> " + received_msg + "<br>";
        messageContainer.innerHTML = message;

        var data = jQuery.parseJSON(received_msg);

        if (data.msg == "response_user_list") {
            $.each(data.users, function (key) {
                var nav = document.getElementById('id_list_ul');
                var text = data.users[key];
                for (var i = 0; i < nav.childNodes.length; i++) {
                    var child = nav.childNodes[i];
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
            var nav = document.getElementById('id_list_ul');
            var text = data.user;
            for (var i = 0; i < nav.childNodes.length; i++) {
                var child = nav.childNodes[i];
                if (text == child.innerText)
                    return;

            }
            if (text.length) {
                $('<li />', {html: text}).bind('click', clickHandler).appendTo('#id_list_ul')
                list.push(text);
            }
        }

        else if (data.msg == "notice_user_removed") {
            var nav = document.getElementById('id_list_ul');
            var button = document.getElementById('id_match_btn');
            var text = data.user;
            for (var i = 0; i < nav.childNodes.length; i++) {
                var child = nav.childNodes[i];
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
            $(".class_lobby").css("display","none");
            $(".class_ingame").css("display","");
            $(".class_gameResult").css("display","none");

            alertify.success("게임 시작!");
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
        json.id = textID.value;
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