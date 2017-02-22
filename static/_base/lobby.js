var Lobby = new Object();

//load elements-----------------------------------------------------
Lobby.message_box = document.getElementById("id_messages");

Lobby.player_list = document.getElementById("id_playerList_ul");
Lobby.match_btn = document.getElementById("id_match_btn");

Lobby.speed_input = document.getElementById("id_setSpeed");

//basic functions for lobby------------------------------------------
Lobby.playerClickHandler = function(event) {
    Lobby.match_btn.disabled='true';

    if (event.target.className == 'class_selected'){
        event.target.className = '';
    } else if (Lobby.countSelectedPlayer() < setting.max_match_cnt){
        event.target.className = 'class_selected';
    }

    if (Lobby.countSelectedPlayer() >= setting.min_match_cnt && Lobby.countSelectedPlayer() <= setting.max_match_cnt) {
        Lobby.match_btn.removeAttribute('disabled');
    }
}

Lobby.countSelectedPlayer = function() {
    var count = 0;
    for(var i = 0; i < Lobby.player_list.childNodes.length; ++i){
        var child = Lobby.player_list.childNodes[i];
        if (child.className == 'class_selected') {
            ++count;
        }
    }
    return count;
}

Lobby.renewPlayerList = function(JSON_data) {
    var users = JSON_data.users;
    $.each(users, function (key) {
        var text = users[key];
        if (text.length) {
            for (var i = 0; i < Lobby.player_list.childNodes.length; i++) {
                var child = Lobby.player_list.childNodes[i];
                if (text == child.innerText) {
                    return;
                }
            }
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(text));
            li.addEventListener("click", Lobby.playerClickHandler);

            if (text == "DUMMY") {
                li.style.color = "blue";
                Lobby.player_list.insertBefore(li, Lobby.player_list.firstChild);
            } else {
                Lobby.player_list.appendChild(li);
            }
        }
    })
}

Lobby.addPlayer = function(JSON_data) {
    var user = JSON_data.user;
    if (user.length) {
        for (var i = 0; i < Lobby.player_list.childNodes.length; i++) {
            var child = Lobby.player_list.childNodes[i];
            if (user == child.innerText) {
                return;
            }
        }
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(user));
        li.addEventListener("click", Lobby.playerClickHandler);

        if (user == "DUMMY") {
            li.style.color = "blue";
            Lobby.player_list.insertBefore(li, Lobby.player_list.firstChild);
        } else {
            Lobby.player_list.appendChild(li);
        }
    }
}

Lobby.removePlayer = function(JSON_data) {
    var user = JSON_data.user;
    if (user.length) {
        for (var i = 0; i < Lobby.player_list.childNodes.length; i++) {
            var child = Lobby.player_list.childNodes[i];
            if (user == child.innerText) {
                child.remove();
            }
        }
    }
    if (Lobby.countSelectedPlayer() < setting.min_match_cnt) {
        Lobby.match_btn.disabled = 'true';
    }
}

Lobby.getMatchResponse = function(JSON_data) {
    loadPage("gameBoard");
}