var baskinMessgae = document.getElementById('id_baskin_message');
var cnt = 0;

var gameMessage = "베스킨라빈스써리원귀엽고깜찍하게써리원" + "<br>";
baskinMessgae.innerHTML = gameMessage;

function recvGameMsg(game_data) {
    if (game_data.msg == "notify_gameloop") {
        gameMessage += game_data.pid + " : ";
        for( var i = 0; i < game_data.num; i++ )
        {
            cnt++;
            gameMessage += cnt + " ";
        }
        gameMessage += "<br>";
        baskinMessgae.innerHTML = gameMessage;
    }
}
