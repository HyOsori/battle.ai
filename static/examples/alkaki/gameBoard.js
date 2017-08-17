GameBoard.size_num = 18;
GameBoard.blank = 3000;
GameBoard.frame = 50;
GameBoard.friction = 100;

GameBoard.board_size = -1;
GameBoard.ratio = -1;
GameBoard.interval = -1;

GameBoard.egg_radius = -1;
GameBoard.egg_count = []; //[black_egg_cnt, white_egg_cnt]

GameBoard.egg_arr;

//-----------------------------------------------------------------------------------------------------------
GameBoard.getReady = function (JSON_data) {
  var game_data = JSON_data.data;
  var player_color = -1;
  var x, y;
  var init_eggs_indices = [];
  GameBoard.egg_arr = new Array();

  for (key in game_data) {
    player_color = game_data[key].color;
    GameBoard.board_size = game_data[key].board_size;
    GameBoard.egg_radius = game_data[key].radius;
    GameBoard.egg_count[player_color] = game_data[key].count;
    init_eggs_indices[player_color] = game_data[key].player_pos;
  }

  GameBoard.ratio = GameBoard.canvas.height / GameBoard.board_size;
  GameBoard.interval = (GameBoard.board_size - GameBoard.blank * 2) / GameBoard.size_num;

  for (var color = 0; color < 2; ++color) {
    init_eggs_indices[color].forEach(function (pos) {
      x = pos[0];
      y = pos[1];
      GameBoard.egg_arr.push(new Egg(x, y, color));
    });
  }

  GameBoard.drawLine();

  for (egg in GameBoard.egg_arr) {
    x = egg.x_pos;
    y = egg.y_pos;
    color = egg.color;
    GameBoard.drawEgg(x, y, color);
  }
};

GameBoard.drawTurnResult = function (JSON_data) {
  var game_data = JSON_data.data;
  var direction = game_data.direction;
  var index = game_data.index;
  var turn = game_data.turn;
  var force = game_data.force;

  var distance = parseInt(Math.sqrt(direction[0] * direction[0] + direction[1] * direction[1]));
  var tmp_x_dir = direction[0] / distance;
  var tmp_y_dir = direction[1] / distance;

  GameBoard.egg_arr[index + turn * this.egg_count[0]].addForce(tmp_x_dir, tmp_y_dir, force);

  GameBoard.is_turn_end = false;

  GameBoard.runPhysics();
  GameBoard.updateBoard();
};

GameBoard.drawLine = function () {
  var ctx = GameBoard.ctx;
  var interval = GameBoard.interval * GameBoard.ratio;
  var blank = GameBoard.blank * GameBoard.ratio;
  var circle_radius = 3;

  ctx.fillStyle = "#ffcc66";
  ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

  // board draw line
  ctx.strokeStyle = "#333300";
  ctx.fillStyle = "#333300";

  for (var i = 0; i < GameBoard.size_num + 1; ++i) {
    // horizontal line draw
    ctx.beginPath();
    ctx.moveTo(blank + i * interval, blank);
    ctx.lineTo(blank + i * interval, GameBoard.canvas.width - blank);
    ctx.stroke();

    // vertical line draw
    ctx.beginPath();
    ctx.moveTo(blank, blank + i * interval);
    ctx.lineTo(GameBoard.canvas.height - blank, blank + i * interval);
    ctx.stroke();
  }

  // board draw point
  for (i = 0; i < 3; i++) {
    for (var j = 0; j < 3; j++) {
      // board circle draw
      ctx.beginPath();
      ctx.arc(blank + 3 * interval + i * 6 * interval, blank + 3 * interval + j * 6 * interval, circle_radius, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();
    }
  }
};

GameBoard.drawEgg = function (x_rate, y_rate, color) {
  var ctx = GameBoard.ctx;
  var x = x_rate * GameBoard.ratio;
  var y = y_rate * GameBoard.ratio;
  var radius = GameBoard.egg_radius * GameBoard.ratio;

  ctx.beginPath();
  if (color == 0) {
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = "black";
    ctx.fill();
  } else if (color == 1) {
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = "white";
    ctx.fill();
  }
  ctx.closePath();
};

function Egg(x_pos, y_pos, color) {
  this.x_pos = x_pos;
  this.y_pos = y_pos;
  this.color = color;
  this.x_dir = 0;
  this.y_dir = 0;
  this.speed = 0;
  this.alive = true;
}

Egg.prototype.addForce = function (x_dir, y_dir, force) {
  this.x_dir = x_dir;
  this.y_dir = y_dir;
  this.speed = force;
  return true;
};

Egg.prototype.isMeet = function (x, y) {
  var radius = GameBoard.egg_radius;
  var distance = Math.sqrt((this.x_pos - x) * (this.x_pos - x) + (this.y_pos - y) * (this.y_pos - y));

  return (distance <= radius * 2) && this.alive && x >= 0 && x <= GameBoard.board_size && y >= 0 && y <= GameBoard.board_size;
};

GameBoard.runPhysics = function () {
  // check_meet use for checking kiss Eggs
  var check_meet;
  for (var i = 0; i < GameBoard.egg_arr.length; ++i) {
    if (GameBoard.egg_arr[i].speed > 0) {
      // Egg Move
      GameBoard.egg_arr[i].x_pos += GameBoard.egg_arr[i].x_dir * GameBoard.egg_arr[i].speed;
      GameBoard.egg_arr[i].y_pos += GameBoard.egg_arr[i].y_dir * GameBoard.egg_arr[i].speed;
      GameBoard.egg_arr[i].speed -= GameBoard.friction; // accelate = ㎍ (friction) -> 50 Frame /50

      for (var j = 0; j < GameBoard.egg_arr.length; ++j) {
        check_meet = false;
        if (j != i) {
          while (GameBoard.egg_arr[i].isMeet(GameBoard.egg_arr[j].x_pos, GameBoard.egg_arr[j].y_pos)) {
            if (!check_meet) {
              check_meet = true;
            }

            if (GameBoard.egg_arr[i].x_pos > GameBoard.egg_arr[j].x_pos) {
              GameBoard.egg_arr[i].x_pos = GameBoard.egg_arr[i].x_pos + Math.abs(GameBoard.egg_arr[i].x_dir);
            } else {
              GameBoard.egg_arr[i].x_pos = GameBoard.egg_arr[i].x_pos - Math.abs(GameBoard.egg_arr[i].x_dir);
            }

            if (GameBoard.egg_arr[i].y_pos > GameBoard.egg_arr[j].y_pos) {
              GameBoard.egg_arr[i].y_pos = GameBoard.egg_arr[i].y_pos + Math.abs(GameBoard.egg_arr[i].y_dir);
            } else {
              GameBoard.egg_arr[i].y_pos = GameBoard.egg_arr[i].y_pos - Math.abs(GameBoard.egg_arr[i].y_dir);
            }
          }

          if (check_meet) {
            // When Kiss Break direction Degree = A
            // When Kiss Other Egg's direction between origin Degree = B
            // Calculate Two Egg's direction and speed
            var kiss_dir_x = (GameBoard.egg_arr[j].x_pos - GameBoard.egg_arr[i].x_pos);
            var kiss_dir_y = (GameBoard.egg_arr[j].y_pos - GameBoard.egg_arr[i].y_pos);
            var distance = Math.sqrt(kiss_dir_x * kiss_dir_x + kiss_dir_y * kiss_dir_y);

            GameBoard.egg_arr[j].x_dir = kiss_dir_x / distance;
            GameBoard.egg_arr[j].y_dir = kiss_dir_y / distance;

            var cosB = (GameBoard.egg_arr[i].x_dir * GameBoard.egg_arr[j].x_dir +
            GameBoard.egg_arr[i].y_dir * GameBoard.egg_arr[j].y_dir);
            var cosA = Math.sqrt(1 - Math.abs(cosB));

            if (cosA < 0.0001 && cosA > 0) cosA = 0.0001;
            if (cosA > -0.0001 && cosA < 0) cosA = -0.0001;
            if (cosB < 0.0001 && cosB > 0) cosB = 0.0001;
            if (cosB > -0.0001 && cosB < 0) cosB = -0.0001;

            GameBoard.egg_arr[i].x_dir = GameBoard.egg_arr[i].x_dir - (GameBoard.egg_arr[j].x_dir) * cosB;
            GameBoard.egg_arr[i].y_dir = GameBoard.egg_arr[i].y_dir - (GameBoard.egg_arr[j].y_dir) * cosB;

            GameBoard.egg_arr[j].speed = GameBoard.egg_arr[i].speed * (1 / (cosA * cosA / cosB + cosB));
            GameBoard.egg_arr[i].speed = GameBoard.egg_arr[i].speed * (1 / (cosB * cosB / cosA + cosA));

          }
        }
      }
    }
  }

  // If Egg have Energy Run Again
  var check_remain_energy = false;

  for (i = 0; i < GameBoard.egg_arr.length; ++i) {
    if (GameBoard.egg_arr[i].speed > 0) {
      check_remain_energy = true;
      break;
    }
  }

  for (i = 0; i < GameBoard.egg_arr.length; ++i) {
    if (GameBoard.egg_arr[i].x_pos < 0 || GameBoard.egg_arr[i].x_pos > GameBoard.board_size ||
      GameBoard.egg_arr[i].y_pos < 0 || GameBoard.egg_arr[i].y_pos > GameBoard.board_size) {
      GameBoard.egg_arr[i].alive = false;
      break;
    }
  }

  if (check_remain_energy) {
    setTimeout(GameBoard.runPhysics, 1000 / GameBoard.frame);

  } else {
    GameBoard.is_turn_end = true;
  }
};

GameBoard.updateBoard = function () {
  var x, y, color;

  GameBoard.drawLine();

  GameBoard.egg_arr.forEach(function (egg) {
    x = egg.x_pos;
    y = egg.y_pos;
    color = egg.color;
    if (egg.alive) {
      GameBoard.drawEgg(x, y, color);
    }
  });

  if (!GameBoard.is_turn_end) {
    setTimeout(GameBoard.updateBoard, 1000 / GameBoard.frame);
  }
};