var MIN_MATCH_USER_CNT = 2;
var MAX_MATCH_USER_CNT = 2;
var Title = "PIXELS";
var xmlhttp = new XMLHttpRequest();

var list = [];
var page_now = "Lobby";

var messageContainer = document.getElementById('id_messages');
var userList = document.getElementById('id_list_ul');
var setSpeed = document.getElementById('id_setSpeed');

$(window).resize(ResizeCanvas);

function checkSelected(){
    var count = 0;
    var dummyClients = document.getElementById('id_dummyclient_ul');
    for(var i=0; i<userList.childNodes.length; i++){
        var child = userList.childNodes[i];
        if (child.className == 'class_selected')
            count++;
    }
    for(var i=0; i<dummyClients.childNodes.length; i++){
        var child = dummyClients.childNodes[i];
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
	//messageContainer.innerHTML = window.location.host
	var ws = new WebSocket("ws://"+window.location.host+"/websocket");

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
                    if (text == "DUMMY") {
                        $('<li />', {html: text}).css("color", "blue").bind('click', clickHandler).appendTo('#id_dummyclient_ul')
                        list.push(text);
                    } else {
                        $('<li />', {html: text}).bind('click', clickHandler).appendTo('#id_list_ul')
                        list.push(text);
                    }
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
                if (text == "DUMMY") {
                    $('<li />', {html: text}).css("color", "blue").bind('click', clickHandler).appendTo('#id_dummyclient_ul')
                    list.push(text);
                } else {
                    $('<li />', {html: text}).bind('click', clickHandler).appendTo('#id_list_ul')
                    list.push(text);
                }
            }
        }

        else if (data.msg == "notice_user_removed") {
            var button = document.getElementById('id_match_btn');
            var text = data.user;
            if (text == "DUMMY") {
                $("#id_dummyclient_ul").empty();
            } else {
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
        }
        /* get log
        else if (data.msg == "") {
            var text = "";
            var log_ul = document.getElementById("id_log");
            var log_li = log_ul.getElementsByTagName("li");
            if (log_li.length >= 10) {
                log_li[10].remove();
            }
            $('<li />', {html: text}).prependTo("#id_log");
        }
        */
        else if (data.msg == "response_match") {
            if (data.data.error == 0) {
                gameStart(data);
                alertify.success("게임 시작!", 2000);
            }
            else {
                alertify.alert("매칭 실패!");
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
                recvGameResult(data.data);
            }
        }

        else if (data.msg == "game_data") {
            if (data.msg_type == "notify_init_loop") {
                loopStart(data.data);
            }
            else if (data.msg_type == "notify_loop") {
                recvTurnResult(data.data);
            }
            else if (data.msg_type == "notify_change_round") {
                recvLoopResult(data.data);
            }
            else if (data.msg_type == "notify_finish") {
                recvRoundResult(data.data);
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

    $("#id_search_btn").bind('click', function() {/*send request search*/
        var input = document.getElementById('id_search_input');
        var keyword = input.value;
        xmlhttp.open("Get","log?name=" + keyword, true);
        xmlhttp.send();
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

xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myArr = JSON.parse(this.responseText);
        GetSearchResults(myArr);
    }
};

function GoToLobby() {
    $(".class_inGame").css("display","none");
    $(".class_gameResult").css("display","none");
    $(".class_lobby").css("display","");

    $("#id_title").html(Title);
    page_now = "Lobby";
}

function GoToInGame() {
    $(".class_lobby").css("display","none");
    $(".class_gameResult").css("display","none");
    $(".class_inGame").css("display","");

    ResizeCanvas();
    page_now = "InGame";
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
    //$("div, button, li").css("font-size", );
    ReadyAfterResize();
}

function GetSearchResults(arr) {
    $("#id_searchResults_ul").empty();
    var text;
    for (var i = 0; i < arr.length; ++i) {
        text = arr[i][1] + " : " + arr[i][2] + " / " + arr[i][3] + " : " + arr[i][4];
        $('<li />', {html: text}).prependTo("#id_searchResults_ul");
    }
}

$("#id_logTab_btn").bind('click', function() {
    $("#id_search").css('display','none');
    $("#id_log").css('display','');
});
$("#id_searchTab_btn").bind('click', function() {
    $("#id_log").css('display','none');
    $("#id_search").css('display','flex');
});

