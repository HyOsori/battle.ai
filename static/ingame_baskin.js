var baskinMessgae = document.getElementById('id_baskin_message');
var cnt = 0;

var gameMessage = "베스킨라빈스써리원귀엽고깜찍하게써리원" + "<br>";
baskinMessgae.innerHTML = gameMessage;


var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

function drawCircle(x,y,color){//draw stone
    ctx.beginPath();
    //arc(x_center,y_center,radius,startAngle,endAngle,anticlockwise)
    var endAngle = Math.PI * 2;
    if (color == 1){
        ctx.arc(35+(50*x),35+(50*y),20,0,endAngle);
        ctx.fillStyle = "black"
        ctx.fill();
    }
    else {
        if (color == 2){
            ctx.arc(35+(50*x),35+(50*y),20,0,endAngle);
            ctx.fillStyle = "white"
            ctx.fill();
            ctx.strokeStyle = "black"
            ctx.stroke();
        }
        else {//erase stone by drawing rect filled with background color
            if (color == 0)
                ctx.clearRect(11+(50*x),11+(50*y),48,48);
        }
    }
    ctx.closePath();
}

for(var i=0; i<5; i++) {
    for(var j=0; j<6; j++) {
        drawCircle(j, i, 2)
    }
}
drawCircle(0, 5, 2)



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
    }
}
function recvGameResult(data) {

}
