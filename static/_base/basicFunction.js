function loadPage(page_name) {
    $(".class_page").find("*").css("display","none");
    $(".class_page").css("display","none");
    $(".class_" + page_name).find("*").css("display","");
    $(".class_" + page_name).css("display","");

    if (page_name == "lobby") {
        return returnJSON("request_user_list", null);
    }
}

function returnJSON(msg, data) {
    var json = new Object();
    var req;

    json.msg = msg;
    json.data = data;
    
    req = JSON.stringify(json);
    return req;
}

function drawText(canvas, text, x, y) {
    if (x < 0 || y < 0) {
        x = 10;
        y = 50;
    }
    var ctx = canvas.getContext('2d');
    ctx.font = '10px serif';
    ctx.fillText(text, x, y);
}

function clearCanvas(canvas) {
    var ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
}

function resizeCanvas(canvas) {
    var canvas_size = $("#id_gameBoard").find(".class_right").innerHeight();
    canvas_size = canvas_size - 20;
    
    var msg_container_size = $("#id_log").width();
    msg_container_size = msg_container_size + 10;
    
    $("#" + canvas.id).attr({"width": canvas_size, "height": canvas_size});
    $("#id_messages").css("width", msg_container_size);
}

function JSONtoString(object) {
    var results = [];
    for (var property in object) {
        var value = object[property];
        if (value)
            results.push(property.toString() + ': ' + value);
        }
                
        return '{' + results.join(', ') + '}';
}