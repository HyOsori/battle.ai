/**
 * Created by First on 2016-07-31.
 */


var canvas = $("#id_board_canvas")[0];
var ctx = canvas.getContext("2d");

//draw lines of board
ctx.beginPath();
for (var i=0; i<9; i++){
    ctx.moveTo(10,10+(50*i));
    ctx.lineTo(410,10+(50*i));
    ctx.stroke();
}
for (var i=0; i<9; i++){
    ctx.moveTo(10+(50*i),10);
    ctx.lineTo(10+(50*i),410);
    ctx.stroke();
}
ctx.closePath();

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

function recvGameMsg(game_data) {
    if (game_data.msg == "notice_board"){
        var y=0;
        $.each(game_data.board,function(){
            for (var x=0; x<8; x++) {
                drawCircle(x,y,this[x]);
            }
            y++;
        })
    }
}