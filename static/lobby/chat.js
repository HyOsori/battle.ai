var ws = new WebSocket("ws://" + window.location.host + "/lobby/socket");
ws.onopen = function(evt){

};
ws.onmessage = function(evt){
    recvChat(JSON.parse(evt.data))
};
ws.onclose = function(){


};

///////보내기


  var msgSendBtn = document.getElementById("Chatting_Click");
msgSendBtn.addEventListener("click", function() {
  var input_box = document.getElementById("Chatting_Real");
  var text = input_box.value;
  var sauce = new Object();
  var chat = new Object();
  var req;

  if(text == ""){
    return;
  }

  chat.name = "Name";
  chat.date = Date.now();
  chat.message = text;

  sauce.msg = "chat";
  sauce.msg_type = "send";
  sauce.data = chat;

  req = JSON.stringify(sauce);
  ws.send(req);
  input_box.value = "";
});

////////////////

function recvChat(JSON_data) {
  var chatting_box = document.getElementById("lobby_chat");
  var li = document.createElement("li");
  var data = JSON_data.data;
  var name = data.name;
  var date = data.date;
  var msg = data.message;
  var text = "(" + date + ")" + name + ": " + msg;
  li.appendChild(document.createTextNode(text));
  chatting_box.appendChild(li);
}
