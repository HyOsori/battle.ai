var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

var round = 1;
var interval = (canvas.width-20)/8;

var users;

//draw lines of board
ctx.beginPath();
for (var i=0; i<9; i++){
    ctx.moveTo(10,10+(interval*i));
    ctx.lineTo(10+(interval*8),10+(interval*i));
    ctx.stroke();
}
for (var i=0; i<9; i++){
    ctx.moveTo(10+(interval*i),10);
    ctx.lineTo(10+(interval*i),10+(interval*8));
    ctx.stroke();
}
ctx.closePath();

function drawCircle(x,y,color){//draw stone
    ctx.beginPath();
    //arc(x_center,y_center,radius,startAngle,endAngle,anticlockwise)
    var endAngle = Math.PI * 2;
    if (color == 1){
        ctx.arc(10+(interval/2)+(interval*x),10+(interval/2)+(interval*y),(interval/2)-5,0,endAngle);
        ctx.fillStyle = "black"
        ctx.fill();
    }
    else if (color == 2){
            ctx.arc(10+(interval/2)+(interval*x),10+(interval/2)+(interval*y),(interval/2)-5,0,endAngle);
            ctx.fillStyle = "white"
            ctx.fill();
            ctx.strokeStyle = "black"
            ctx.stroke();
    }
    else if (color == 0)
        ctx.clearRect(11+(interval*x),11+(interval*y),interval-2,interval-2);
    ctx.closePath();
}

function highLight(x,y,color){
    ctx.beginPath();
    if (color == 1){
        ctx.fillStyle = "white"
        ctx.fillRect(10+(interval*0.45)+(interval*x),10+(interval*0.45)+(interval*y),interval*0.1,interval*0.1);
    }
    else if (color == 2){
        ctx.fillStyle = "black"
        ctx.fillRect(10+(interval*0.45)+(interval*x),10+(interval*0.45)+(interval*y),interval*0.1,interval*0.1);
    }
    ctx.closePath();
}

function gameStart(user_list) {
    users = user_list;
    $("#id_gameMessage").html("● "+users[0]+"  vs  "+users[1]+" ○").css("text-align","center");
    $("#id_gameMessage_second").html("Round "+round);
}

function recvGameMsg(data) {
    if (data.msg_type == "notify_on_turn") {
        var y=0;
        $.each(data.game_data.board,function(){
            for (var x=0; x<8; x++) {
                drawCircle(x,y,this[x]);
            }
            y++;
        })
    }
}
function recvGameResult(data) {
    for (var key in data.game_data ) {
        if (data.game_data[key] == "win") {
            alertify.alert(key + " 승리!")
            $("#id_gameMessage").html(key+" WIN!").css("text-align","center");
        }
        else if (data.game_data[key] == "draw") {0
            alertify.alert("무승부!")
            $("#id_gameMessage").html("DRAW").css("text-align", "center");
        }
    }
    goToGameResult();
}