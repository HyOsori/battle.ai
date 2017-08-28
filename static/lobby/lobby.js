var ws = new WebSocket("ws://" + window.location.host + "/lobby/socket");
ws.onopen = function(evt){
  var gamelog = new Object();
  var user = new Object();
  var set1,set2;

  gamelog.msg = "gamelog";
  gamelog.msg_type = "init";
  user.msg = "user";
  user.msg_type = "init";

  set1 = JSON.stringify(gamelog);
  set2 = JSON.stringify(user);
  ws.send(set1);
  ws.send(set2);
};
ws.onmessage = function(evt){
    var checker;
    checker = JSON.parse(evt.data);

    if(checker.msg == "gamelog" && checker.msg_type == "init"){
      firstrecvLog(JSON.parse(evt.data));
    }
    else if(checker.msg == "chat"){
      recvChat(JSON.parse(evt.data));
    }
    else if(checker.msg == "gamelog"){
      recvLog(JSON.parse(evt.data));
    }
    else if(checker.msg == "user" && checker.msg_type == "init"){
      firstUser(JSON.parse(evt.data));
    }
    else if(checker.msg == "user"){
      useradd(JSON.parse(evt.data));
    }
};
ws.onclose = function(){


};

///////(아래)기본 세팅
var _id = new Array();
var AI_count = 0;
var AI_List1 = "";
var AI_List2 = "";

///////(아래)채팅 보내기
var msgSendBtn = document.getElementById("Chatting_Click");
msgSendBtn.addEventListener("click", function() {
    var input_box = document.getElementById("Chatting_Real");
    var text = input_box.value;
    var sauce = new Object();
    var chat = new Object();
    var req;
    var day = new Date();
    var days = new Array();
    var dayer;
    days[0] = String(day.getHours());
    days[1] = String(day.getMinutes());
    dayer = days[0] + days[1];
    dayer = Number(dayer);

    if(text == ""){
        return;
    }

    chat.name = "Name";
    chat.date = dayer;
    chat.message = text;

    sauce.msg = "chat";
    sauce.msg_type = "send";
    sauce.data = chat;

    req = JSON.stringify(sauce);
    ws.send(req);
    input_box.value = "";
});

///////(아래)채팅창에 나타내기
function recvChat(JSON_data) {
  var chatting_box = document.getElementById("lobby_chat");
  var li = document.createElement("li");
  var data = JSON_data.data;
  var name = data.name;
  var date = data.date;
  var msg = data.message;
  var Hour = parseInt(date / 100);
  var Minute = date % 100;
  var text = "[" + Hour + ":" + Minute + "]" + name + ": " + msg;
  li.appendChild(document.createTextNode(text));
  chatting_box.appendChild(li);
}

///////(아래)로그창에 나타내기
function recvLog(JSON_data) {
    var log_box = document.getElementById("lobby_log");
    var li = document.createElement("li");
    var data = JSON_data.data;
    var id = data._id;
    _id.push(id);
    var game_result = data.game_result;
    var players = new Array();
    players = data.players;
    var checker = new Array();
    checker = game_result.winner;
    if (checker[0] != null){
        li.addEventListener("click", function(){clickListGameLog(id)}, false);
      var text = "[" + "승자 : " + checker[0] + "] " + players[0] + " VS. " + players[1];
      li.appendChild(document.createTextNode(text));
      log_box.appendChild(li);
    }
    else {
        li.addEventListener("click", function(){clickListGameLog(id)}, false);
        var text = "[" + "무승부! " + "] " + players[0] + " VS. " + players[1];
        li.appendChild(document.createTextNode(text));
        log_box.appendChild(li);
    }

}

///////(아래) AImatch 시킬 경우 "POST"로 데이터 전송
function AImatch(AI1, AI2) {
  $.ajax({
    type: 'POST',
    async: true,
    url: '/lobby/game/request',
    data: {
        players: 'hi',
        type: 'user',
    },
    dataType : 'json'
  });
}

///////(아래) log 눌렀을 경우 "POST" 로 데이터 전송
function clickListGameLog(_id) {
    $.post("lobby/game/request", {type: "gamelog", _id: _id},
        function (val) {
            location.replace("/game?type=" + "gamelog" + "&_id=" + _id)
        });
}

//////(아래) log 창에 처음 결과 나타낼때
function firstrecvLog(JSON_data) {
  var log_box = document.getElementById("lobby_log");
  var data = JSON_data.data;
  var vi = document.createElement("li");
  var up_text = "여태까지 진행된 경기";
  vi.appendChild(document.createTextNode(up_text));
  log_box.appendChild(vi);
  data.forEach(function(num){
    var li = document.createElement("li");
    li.addEventListener("click", function(){clickListGameLog(num._id)}, false);
    text = "[" + "승자 : " + num.game_result["winner"][0] + "] " + num.players[0] + " VS. " + num.players[1] ;
    li.appendChild(document.createTextNode(text));
    log_box.appendChild(li);
  });
}

//////(아래) User 가 처음 들어왔을때
function firstUser(JSON_data){
  var log_box = document.getElementById("lobby_AIlist");
  var data = JSON_data.data;
  data.forEach(function(num){
    var li = document.createElement("li");
    li.addEventListener("click", function(){AI_versus(li, num)}, false);
    li.appendChild(document.createTextNode(num));
    log_box.appendChild(li);
  });
}

///////(아래) USER 가 add 되었을때
function useradd(JSON_data){
  var log_box = document.getElementById("lobby_AIlist");
  var li = document.createElement("li");
  var data = JSON_data.data;
  li.addEventListener("click", function(){AI_versus(li, data)}, false);
  li.appendChild(document.createTextNode(data));
  log_box.appendChild(li);
}

///////(아래) AI list 에서 매치시킬때 함수
function Matcher(){
    if(AI_List1 != "" && AI_List2 != ""){
        AImatch(AI_List1, AI_List2);
        alert('매치 시작!!');
    }
    else if (AI_List1 == "" && AI_List2 == ""){
        alert("두 명더 선택해 주십시오.");
    }
    else if (AI_List1 == "" || AI_List2 == ""){
        alert("한 명더 선택해 주십시오.");
    }
}

///////(아래) AI Click & Match 기능 구현 함수
function AI_versus(list, name){
    if (AI_List1 == name){
        AI_List1 = "";
        AI_count--;
        changeList_B(list);
    }
    else if(AI_List2 == name){
        AI_List2 = "";
        AI_count--;
        changeList_B(list);
    }
    else if (AI_count == 0 && AI_List1 == "" && AI_List2 == ""){
        AI_List1 = name;
        AI_count++;
        changeList_A(list);
    }
    else if (AI_count == 1 && AI_List1 != "" && AI_List2 == ""){
        AI_List2 = name;
        AI_count++;
        changeList_A(list);
    }
    else if(AI_count == 1 && AI_List1 == "" && AI_List2 != ""){
        AI_List1 = name;
        AI_count++;
        changeList_A(list);
    }
}

///////(아래) AI list 클릭시 색 변환함수 (누른경우)
function changeList_A(list){
    list.style.background = "yellow";
}

///////(아래) AI list 클릭시 색 변환함수 (푼경우)
function changeList_B(list){
    list.style.background = "red";
}