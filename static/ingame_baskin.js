var baskinMessgae = document.getElementById('id_baskin_message');
var cnt = 0;

var gameMessage = "베스킨라빈스써리원귀엽고깜찍하게써리원" + "<br>";
baskinMessgae.innerHTML = gameMessage;

function recvGameMsg(data) {
    if (data.msg_type == "notify_gameloop") {
        gameMessage += data.game_data.pid + " : ";
        for( var i = 0; i < data.game_data.num; i++ )
        {
            cnt++;
            gameMessage += cnt + " ";
        }
        gameMessage += "<br>";
        baskinMessgae.innerHTML = gameMessage;
    }
    else if (data.msg_type == "round_result") {
        gameMessage += "-------------------------" + "<br>";
        for (var key in data.game_data )
        {
            gameMessage += key + " ";
            if (data.game_data[key] == "win")
                gameMessage += "승리";
            else
                gameMessage += "패배";
            gameMessage += "<br>";
        }
        gameMessage += "-------------------------" + "<br>";
        baskinMessgae.innerHTML = gameMessage;

        cnt = 0;
    }
}
function recvGameResult(data) {
    gameMessage += "<br>";
    for (var key in data.game_data )
    {
        gameMessage += key + " ";
        if (data.game_data[key] == "win")
            gameMessage += "최종 승리";
        else
            gameMessage += "최종 패배";
        gameMessage += "<br>";
    }
    baskinMessgae.innerHTML = gameMessage;
}
