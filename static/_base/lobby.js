
//load elements-----------------------------------------------------
var message_box = document.getElementsByClassName("class_messages");

var player_list = document.getElementById("id_playerList_ul");
var match_btn = document.getElementById("id_match_btn");

var speed_input = document.getElementById("id_setSpeed");

//basic functions for lobby------------------------------------------
function playerClickHandler() {
    match_btn.disabled='true';

    if (event.target.className == 'class_selected'){
        event.target.className = '';
    } else if (countSelectedPlayer() < setting.max_match_cnt){
        event.target.className = 'class_selected';
    }

    if (countSelectedPlayer() >= setting.min_match_cnt && countSelectedPlayer() <= setting.max_match_cnt) {
        match_btn.removeAttribute('disabled');
    }
}

function countSelectedPlayer() {
    var count = 0;
    for(var i = 0; i < player_list.childNodes.length; ++i){
        var child = player_list.childNodes[i];
        if (child.className == 'class_selected') {
            ++count;
        }
    }
    return count;
}

function renewPlayerList(JSON_data) {
    var users = JSON_data.users;
    $.each(users, function (key) {
        var text = users[key];
        if (text.length) {
            for (var i = 0; i < player_list.childNodes.length; i++) {
                var child = player_list.childNodes[i];
                if (text == child.innerText) {
                    return;
                }
            }
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(text));
            li.addEventListener("click", playerClickHandler);

            if (text == "DUMMY") {
                li.style.color = "blue";
                player_list.insertBefore(li, player_list.firstChild);
            } else {
                player_list.appendChild(li);
            }
        }
    })
}

function addPlayer(JSON_data) {
    var user = JSON_data.user;
    if (user.length) {
        for (var i = 0; i < player_list.childNodes.length; i++) {
            var child = player_list.childNodes[i];
            if (user == child.innerText) {
                return;
            }
        }
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(text));
        li.addEventListener("click", playerClickHandler);

        if (user == "DUMMY") {
            li.style.color = "blue";
            player_list.insertBefore(li, player_list.firstChild);
        } else {
            player_list.appendChild(li);
        }
    }
}

function removePlayer(JSON_data) {
    var user = JSON_data.user;
    if (user.length) {
        for (var i = 0; i < player_list.childNodes.length; i++) {
            var child = player_list.childNodes[i];
            if (user == child.innerText) {
                child.remove();
            }
        }
    }
    if (countSelectedPlayer() < setting.min_match_cnt) {
        match_btn.disabled = 'true';
    }
}

function getMatchResponse(JSON_data) {
    loadPage("gameBoard");
}