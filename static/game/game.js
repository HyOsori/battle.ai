const Game = React.createClass({
  componentDidMount: function(){
    this.turn_results = new Queue();
    this.connection = new WebSocket("ws://" + window.location.host + "/websocket");
    this.connection.onmessage = evt => {
      console.log("message: " + evt.data);
      var data = jQuery.parseJSON(evt.data);
      if (data.msg == "notice_user_added" && data.user == "AI2") {
        this.match("AI1", "AI2");
      } else if (data.msg == "response_match") {
        /**
         *    msg : response_match
         *    msg_type : null
         *
         *    data
         *    speed : 0,1
         *    users : [(string), (string),...]
         */
      } else if (data.msg == "game_handler") {
        if (data.msg_type == "ready") {
          /**
           *    msg : game_handler
           *    msg_type : ready
           *
           *    data(alkaki)
           *    { AI_name : { init_data }, AI_name : { init_data }}
           *
           *    init_data(alkaki)
           *    radius : (integer)
           *    color : 0(black) or 1(white)
           *    board_size : (integer)
           *    player_pos : [[x0, y0], [x1, y1], ... ]
           *    count : (integer)
           */
          
          this.board.getReady(data);

        } else if (data.msg_type == "end") {
          /**
           *    msg : game_handler
           *    msg_type : end
           *
           *    data
           *    winner : [(string)]
           */
          var turn_data = this.turn_results;
          
          var drawing = setInterval(function() {
            if (turn_data.isEmpty()) {
                clearInterval(drawing);
                alertify.alert(data.data['winner'][0] + ' 승리!');
                setTimeout("console.log('로비로 돌아갑니다.')", 2000);
                return;
            }

            if (this.board.state.is_turn_end) {
              this.board.drawTurnResult(turn_data.dequeue());
            }
          }, 0);
        }
      } else if (data.msg == "game_data") {
        if (data.msg_type == "game") {
          /**
           *    msg : game_data
           *    msg_type : game
           *
           *    data(alkaki)
           *    index : (integer)
           *    turn : 0(black) or 1(white)
           *    direction : [x, y]
           *    force : (integer)
           */

          this.board.drawTurnResult(data);
        }
      }
    };
    this.connection.onopen = evt => {
      /*
        var json = new Object();
        var req;
        json.msg = "request_user_list";
        req = JSON.stringify(json);
        this.connection.send(req);
      */
    }
  },
  match: function(player1, player2) {
    var json = new Object();
    var data = new Object();
    var req;
    json.msg = "request_match";
    data.users = [player1, player2];
    data.speed = "2";
    json.data = data;
    req = JSON.stringify(json);
    this.connection.send(req);
  },
  saveTurnResult: function(JSON_data) {
    this.state.turn_results.enqueue(JSON_data);
  },
  render: function() {
    return (
      <div>
        <Board players={ this.props.players } ref={ instance => { this.board = instance; }}/>
      </div>
    );
  }
});

Game.defaultProps = {
  players: ["PLAYER1", "PLAYER2"]
};

const Board = React.createClass({
  getInitialState: function(){
    return {
      is_turn_end: true,

      frame: 50,
      board_size_num: 18,
      margin_size_rate: 3,
      dot_size: 3,

      board_size_rate: -1,
      board_ratio: -1,
      line_interval_rate: -1,
      egg_radius_rate: -1,
      
      egg_cnt: [],                //black_cnt, white_cnt
      egg_pos: []                 //[Egg, Egg, ...]
    }
  },
  drawLine: function() {
    var canvas = document.getElementById("board");
    var ctx = canvas.getContext("2d");
    var interval = this.state.line_interval_rate * this.state.board_ratio;
    var blank = this.state.margin_size_rate * this.state.board_ratio;
    var circle_radius = this.state.dot_size;

    ctx.fillStyle="#ffcc66";
	  ctx.fillRect(0, 0, canvas.width, canvas.height);

    // board draw line
	  ctx.strokeStyle="#333300";
	  ctx.fillStyle="#333300";

	  for (var i = 0; i < this.state.board_size_num + 1; ++i) {
      // horizontal line draw
      ctx.beginPath();
      ctx.moveTo(blank + i * interval, blank);
      ctx.lineTo(blank + i * interval, canvas.width - blank);
      ctx.stroke();

      // vertical line draw
      ctx.beginPath();
      ctx.moveTo(blank, blank + i * interval);
      ctx.lineTo(canvas.height - blank, blank + i * interval);
      ctx.stroke();
    }

    // board draw point
    for (i = 0; i < 3; i++) {
      for (var j = 0; j < 3; j++) {
        ctx.beginPath();
        ctx.arc(blank + 3 * interval + i * 6 * interval, blank + 3 * interval + j * 6 * interval, circle_radius, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
      }
    }
  },
  drawEgg: function(x_rate, y_rate, color) {
    var canvas = document.getElementById("board");
    var ctx = canvas.getContext("2d");
    var x = x_rate * this.state.board_ratio;
    var y = y_rate * this.state.board_ratio;
    var radius = this.state.egg_radius_rate * this.state.board_ratio;

    ctx.beginPath();
    if (color == 0) {
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = "black";
        ctx.fill();
    } else if (color == 1){
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fillStyle = "white";
        ctx.fill();
    }
    ctx.closePath();
  },
  getReady: function(JSON_data) {
    var canvas = document.getElementById("board");
    var game_data = JSON_data.data;
    var player_color = -1;
    var x, y;
    var init_eggs_indices = [];

    this.state.egg_pos = new Array();

    for (key in game_data) {
      player_color = game_data[key].color;
      this.state.board_size_rate = game_data[key].board_size;
      this.state.egg_radius_rate = game_data[key].radius;
      this.state.egg_cnt[player_color] = game_data[key].count;
      game_data[key].player_pos.forEach(pos => {
        x = pos[0];
        y = pos[1];
        this.state.egg_pos.push(new Egg(x, y, player_color));
      })
    }

    this.state.board_ratio = canvas.height / this.state.board_size_rate;
    this.state.line_interval_rate = (this.state.board_size_rate - this.state.margin_size_rate * 2) / this.state.board_size_num;

    this.drawLine();
    
    this.state.egg_pos.forEach(egg => {
      console.log(egg);
      x = egg.x_pos;
      y = egg.y_pos;
      color = egg.color;
      this.drawEgg(x, y, color);
    })
  },
  drawTurnResult: function(JSON_data) {
    var game_data = JSON_data.data;
    var direction = game_data.direction;
    var index = game_data.index;
    var turn = game_data.turn;
    var force = game_data.force;

	  this.state.egg_pos[index + turn * this.state.egg_cnt[0]].addForce(direction[0], direction[1], force);

	  this.state.is_turn_end = false;

    console.log("drawTurnResult!");
	  /*
	  runPhysics();
	  updateBoard();
	  */
  },
  render: function() {
    return (
      <section id="center">
        <h3>
          <span>&#9899; </span>
          {this.props.players.map((name, i) => {
              if (i >= this.props.players.length - 1) { return (<span key={i}>{name}</span>); }
              else { return (<span key={i}>{name} vs </span>); }
          })}
          <span> &#9898;</span>
        </h3>
        <section id>
          <canvas id="board" width="480" height="480">Your Browser does not support Canvas!</canvas>
        </section>
      </section>
    );
  }
});



function Egg(x_pos, y_pos, color) {
	this.x_pos = x_pos;
	this.y_pos = y_pos;
	this.color = color;
	this.x_dir = 0;
	this.y_dir = 0;
	this.speed = 0;
	this.alive = true;
}

Egg.prototype.addForce = function(x_dir, y_dir, force) {
	this.x_dir = x_dir;
	this.y_dir = y_dir;
	this.speed = force;
	return true;
};

Egg.prototype.isMeet = function(x, y) {
  var radius = GameBoard.egg_radius;
  var distance = Math.sqrt((this.x_pos - x) * (this.x_pos - x) + (this.y_pos - y) * (this.y_pos - y));

  return (distance <= radius * 2) && this.alive && x >= 0 && x <= Board.state.board_size_rate && y >= 0 && y <= Board.state.board_size_rate;
};

React.render(<Game/>, document.getElementById('Game'));