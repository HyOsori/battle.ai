var baskinMessgae = document.getElementById('id_baskin_message');
var cnt = 0;
var users;
var users_color = ["Peru", "Pink", "Plum", "PowderBlue", "Purple", "Red", "RosyBrown",
                    "ROyalBlue", "SaddleBrown","Salmon"];
var users_win_count = []

var gameMessage = "베스킨라빈스써리원귀엽고깜찍하게써리원" + "<br>";
baskinMessgae.innerHTML = gameMessage;


var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");
ctx.font = "20px Arial";

function drawCircle(x,y,color){//draw stone
    ctx.beginPath();
    //arc(x_center,y_center,radius,startAngle,endAngle,anticlockwise)
    var endAngle = Math.PI * 2;
    if (color == 1){
        ctx.arc(35+(50*x),35+(50*y),20,0,endAngle);
        ctx.fillStyle = "black"
        ctx.fill();
    }
    else if (color == 2){
        ctx.arc(35+(50*x),35+(50*y),20,0,endAngle);
        ctx.fillStyle = "white"
        ctx.fill();
        ctx.strokeStyle = "black"
        ctx.stroke();
    }else if(color == 0){//erase stone by drawing rect filled with background color
        ctx.clearRect(11+(50*x),11+(50*y),48,48);
    }else{
        ctx.arc(35+(50*x),35+(50*y),20,0,endAngle);
        ctx.fillStyle = color
        ctx.fill();
    }

    ctx.closePath();
}



function initBoard(){
    for(var i=0; i<6; i++) {
        for(var j=0; j<5; j++) {
            drawCircle(j, i, 2);
        }
    }
    drawCircle(0, 6, 2)
}
initBoard()

function gameStart(user_list) {
    users = user_list;
    for(var i=0; i< users.length; i++){
        drawCircle(8,i, users_color[i]);
        // ctx.fillStyle = "black"
        // ctx.fill();
        // ctx.fillText(users[i], 430, 50*i);
    }
    // for(var user in users){
    //     drawCircle(8,0)
    // }
    //user 색 설정
    //user 색 및 플레이어 이름 출력
}

function getIndexFromData(data, l) {
    for(var i=0; i < l.length; i++) {
        if (l[i] == data)
            return i;
    }
}

function recvGameMsg(data) {
    if (data.msg_type == "notify_gameloop") {
        gameMessage += data.game_data.pid + " : ";
        user_color = users_color[getIndexFromData(data.game_data.pid, users)]
        for( var i = 0; i < data.game_data.num; i++ )
        {
            cnt++;

            gameMessage += cnt + " ";
            drawCircle((cnt-1)%5, parseInt(((cnt-1)/5)), user_color)
            console.info(((cnt-1)%5+1) + ", " +((cnt-1)/5+1))
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
        initBoard()
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
