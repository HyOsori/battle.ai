window.onload = function() {
    if ("WebSocket" in window) {
        var ws = new WebSocket("ws://" + window.location.host + "/websocket");
        var message = "";
        ws.onopen = function(evt) {
            ws.send(loadPage("lobby"));
        };
        ws.onmessage = function(evt) {
            var received_msg = evt.data;
            var data = jQuery.parseJSON(received_msg);
            var request;

            console.log(received_msg);
            message += ">> " + received_msg + "<br>";
            message_box.innerHTML = message;

            if (typeof setting.protocol[data.msg] == "function") {
                request = setting.protocol[data.msg](data);
            } else {
                request = setting.protocol[data.msg][data.msg_type](data);
            }
            
            if (typeof request != "undefined") {
                ws.send(request);
            }
        };
        ws.onclose = function() {
            message = "";
            message_box.innerHTML = "Connection is closed...";
        };
        
        $('#id_match_btn').bind('click',function() {
            var selectedPlayers = [];
            var speed = speed_input.value;
            var data = new Object();
            for (var i = 0; i < player_list.childNodes.length; ++i){
                var child = player_list.childNodes[i];
                if (child.className == 'class_selected'){
                    selectedPlayers.push(child.innerText);
                }
            }
            data.users = selectedPlayers;
            data.speed = speed;
            
            ws.send(returnJSON("request_match", data));
        });
    } else {
        message_box.innerHTML = "WebSocket NOT supported by your Browser!";
    }
};