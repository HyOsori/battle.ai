const Game = React.createClass({
    getInitialState: function () {
        return {
            is_game_end: false
        }
    },
    componentDidMount: function () {
        this.turn_results = new Queue();
        this.connection = new WebSocket("ws://" + window.location.host + "/game/socket");
        this.connection.onmessage = evt => {
            console.log("message: " + evt.data);
            var data = jQuery.parseJSON(evt.data);
            if (data.msg === "response_match") {
                /**
                 *    msg : response_match
                 *    msg_type : null
                 *
                 *    data
                 *    speed : 0,1
                 *    users : [(string), (string),...]
                 */
            } else if (data.msg === "game_handler") {
                if (data.msg_type === "ready") {
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

                } else if (data.msg_type === "end") {
                    /**
                     *    msg : game_handler
                     *    msg_type : end
                     *
                     *    data
                     *    winner : [(string)]
                     */
                    this.state.is_game_end = true;

                    var is_end = this.state.is_game_end;
                    var turn_data = this.turn_results;
                    var board = this.board;

                    var drawing = setInterval(function () {
                        if (is_end) {
                            // 디버깅 할 때 한프레임씩 볼 수 있다
                            //board.funcSleep(200);
                            if (turn_data.isEmpty()) {
                                clearInterval(drawing);
                                alertify.alert('<b>' + data.data['winner'][0] + ' 승리!</b><br>잠시 후 로비로 돌아갑니다.');
                                setTimeout("window.location.replace('/lobby')", 3000);
                                return;
                            }

                            if (board.getTurnEnd()) {
                                board.drawTurnResult(turn_data.dequeue());
                            }
                        }
                    }, 0);
                }
            } else if (data.msg === "game_data") {
                if (data.msg_type === "game") {
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

                    this.saveTurnResult(data);
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
            this.match();
        }
    },
    match: function () {
        var json = new Object();
        var data = new Object();
        var req;
        json.msg = "gamehandler";
        json.msg_type = "match";

        data.type = this.props.type;
        data.players = this.props.players;
        data._id = this.props._id;

        json.data = data;

        req = JSON.stringify(json);
        this.connection.send(req);
    },
    saveTurnResult: function (JSON_data) {
        this.turn_results.enqueue(JSON_data);
    },
    render: function () {
        return (
            <div>
                <Board players={ this.props.players } ref={ instance => {
                    this.board = instance;
                }}/>
            </div>
        );
    }
});

const Board = React.createClass({
    getInitialState: function () {
        return {
            players: [],

            is_turn_end: true,

            frame: 50,
            friction: 1000,
            board_size_num: 18,
            margin_size_rate: 30000,
            dot_size: 3,

            board_size_rate: -1,
            board_ratio: -1,
            line_interval_rate: -1,
            egg_radius_rate: -1,

            egg_cnt: [],                //black_cnt, white_cnt
            egg_pos: []                 //[Egg, Egg, ...]
        }
    },
    getTurnEnd: function () {
        return this.state.is_turn_end;
    },
    drawLine: function () {
        var canvas = document.getElementById("board");
        var ctx = canvas.getContext("2d");
        var interval = this.state.line_interval_rate * this.state.board_ratio;
        var blank = this.state.margin_size_rate * this.state.board_ratio;
        var circle_radius = this.state.dot_size;

        ctx.fillStyle = "#ffcc66";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // board draw line
        ctx.strokeStyle = "#333300";
        ctx.fillStyle = "#333300";

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
    drawEgg: function (x_rate, y_rate, color) {
        var canvas = document.getElementById("board");
        var ctx = canvas.getContext("2d");
        var x = x_rate * this.state.board_ratio;
        var y = y_rate * this.state.board_ratio;
        var radius = this.state.egg_radius_rate * this.state.board_ratio;

        ctx.beginPath();
        if (color === 0) {
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fillStyle = "black";
            ctx.fill();
        } else if (color === 1) {
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fillStyle = "white";
            ctx.fill();
        }
        ctx.closePath();
    },
    getReady: function (JSON_data) {
        var canvas = document.getElementById("board");
        var game_data = JSON_data.data;
        var player_color = -1;
        var x, y;
        var init_eggs_indices = [];
        var users = [];

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
            });
            users[player_color] = key;
        }

        this.setState({ players: users });

        this.state.board_ratio = canvas.height / this.state.board_size_rate;
        this.state.line_interval_rate = (this.state.board_size_rate - this.state.margin_size_rate * 2) / this.state.board_size_num;

        this.drawLine();

        for (var i = 0; i < this.state.egg_pos.length; ++i) {
            egg = this.state.egg_pos[i];
            x = egg.x_pos;
            y = egg.y_pos;
            color = egg.color;
            this.drawEgg(x, y, color);
        }
    },
    drawTurnResult: function (JSON_data) {
        var game_data = JSON_data.data;
        var direction = game_data.direction;
        var index = game_data.index;
        var turn = game_data.turn;
        var force = game_data.force;
        var color_index = this.state.egg_pos[0].color === turn ? 0 : 5;
        var distance = Math.sqrt(direction[0] * direction[0] + direction[1] * direction[1]);

        this.state.egg_pos[color_index + index].addForce(direction[0] / distance, direction[1] / distance, force);

        this.state.is_turn_end = false;

        this.runPhysics();
        this.updateBoard();
    },
    runPhysics: function () {
        // check_meet use for checking kiss Eggs
        var check_meet;
        for (var i = 0; i < this.state.egg_pos.length; ++i) {
            if (this.state.egg_pos[i].speed > 0 && this.state.egg_pos[i].alive) {

                var distance_dir = Math.sqrt(Math.pow(this.state.egg_pos[i].x_dir, 2) +
                    Math.pow(this.state.egg_pos[i].y_dir, 2));

                this.state.egg_pos[i].speed = Math.floor(this.state.egg_pos[i].speed);

                if (distance_dir < 0.0000001 || this.state.egg_pos[i].speed < 5) {
                    this.state.egg_pos[i].speed = 0;
                    continue;
                }

                this.state.egg_pos[i].x_dir = this.state.egg_pos[i].x_dir / distance_dir;
                this.state.egg_pos[i].y_dir = this.state.egg_pos[i].y_dir / distance_dir;

                // Egg Move
                this.state.egg_pos[i].x_pos += Math.floor(this.state.egg_pos[i].x_dir * this.state.egg_pos[i].speed);
                this.state.egg_pos[i].y_pos += Math.floor(this.state.egg_pos[i].y_dir * this.state.egg_pos[i].speed);
                this.state.egg_pos[i].speed -= this.state.friction; // accelate = ㎍ (friction) -> 50 Frame /50

                for (var j = 0; j < this.state.egg_pos.length; ++j) {
                    check_meet = false;
                    if (j !== i) {
                        while (this.state.egg_pos[i].isMeet(this.state.egg_pos[j].x_pos, this.state.egg_pos[j].y_pos,
                            this.state.egg_radius_rate, this.state.board_size_rate)) {
                            if (!check_meet) {
                                check_meet = true;
                            }

                            if (this.state.egg_pos[i].x_pos > this.state.egg_pos[j].x_pos) {
                                this.state.egg_pos[i].x_pos += (Math.abs(this.state.egg_pos[i].x_dir * 10000) + 1);
                                this.state.egg_pos[i].x_pos = Math.floor(this.state.egg_pos[i].x_pos);
                            } else {
                                this.state.egg_pos[i].x_pos -= (Math.abs(this.state.egg_pos[i].x_dir * 10000) + 1);
                                this.state.egg_pos[i].x_pos = Math.floor(this.state.egg_pos[i].x_pos);
                            }

                            if (this.state.egg_pos[i].y_pos > this.state.egg_pos[j].y_pos) {
                                this.state.egg_pos[i].y_pos += (Math.abs(this.state.egg_pos[i].y_dir * 10000) + 1);
                                this.state.egg_pos[i].y_pos = Math.floor(this.state.egg_pos[i].y_pos);
                            } else {
                                this.state.egg_pos[i].y_pos -= (Math.abs(this.state.egg_pos[i].y_dir * 10000) + 1);
                                this.state.egg_pos[i].y_pos = Math.floor(this.state.egg_pos[i].y_pos);
                            }

                        }

                        if (check_meet) {
                            // When Kiss Break direction Degree = A
                            // When Kiss Other Egg's direction between origin Degree = B
                            // Calculate Two Egg's direction and speed
                            var kiss_dir_x = (this.state.egg_pos[j].x_pos - this.state.egg_pos[i].x_pos);
                            var kiss_dir_y = (this.state.egg_pos[j].y_pos - this.state.egg_pos[i].y_pos);


                            var distance = Math.sqrt(kiss_dir_x * kiss_dir_x + kiss_dir_y * kiss_dir_y);

                            this.state.egg_pos[j].x_dir = kiss_dir_x / distance;
                            this.state.egg_pos[j].y_dir = kiss_dir_y / distance;

                            var cosB = (this.state.egg_pos[i].x_dir * this.state.egg_pos[j].x_dir +
                            this.state.egg_pos[i].y_dir * this.state.egg_pos[j].y_dir);
                            var cosA = Math.sqrt(1 - Math.abs(cosB));

                            if (cosA < 0.0001 && cosA > 0) cosA = 0.0001;
                            if (cosA > -0.0001 && cosA < 0) cosA = -0.0001;
                            if (cosB < 0.0001 && cosB > 0) cosB = 0.0001;
                            if (cosB > -0.0001 && cosB < 0) cosB = -0.0001;


                            this.state.egg_pos[i].x_dir = this.state.egg_pos[i].x_dir - (this.state.egg_pos[j].x_dir) * cosB;
                            this.state.egg_pos[i].y_dir = this.state.egg_pos[i].y_dir - (this.state.egg_pos[j].y_dir) * cosB;

                            if (cosB === 0)
                                this.state.egg_pos[j].speed = 0;
                            else
                                this.state.egg_pos[j].speed = Math.floor(this.state.egg_pos[i].speed * (1 / (cosA * cosA / cosB + cosB)));

                            if (cosA === 0)
                                this.state.egg_pos[i].speed = 0;
                            else
                                this.state.egg_pos[i].speed = Math.floor(this.state.egg_pos[j].speed * (1 / (cosB * cosB / cosA + cosA)));

                        }
                    }
                }
            }
        }

        // If Egg have Energy Run Again
        var check_remain_energy = false;

        for (i = 0; i < this.state.egg_pos.length; ++i) {
            if (this.state.egg_pos[i].x_pos < 0 || this.state.egg_pos[i].x_pos > this.state.board_size_rate ||
                this.state.egg_pos[i].y_pos < 0 || this.state.egg_pos[i].y_pos > this.state.board_size_rate) {
                this.state.egg_pos[i].alive = false;
            }
        }

        for (i = 0; i < this.state.egg_pos.length; ++i) {
            if (this.state.egg_pos[i].speed > 0 && this.state.egg_pos[i].alive) {
                check_remain_energy = true;
                break;
            }
        }

        if (check_remain_energy) {
            setTimeout(this.runPhysics, 1000 / this.state.frame);
        } else {
            this.state.is_turn_end = true;
        }
    },
    updateBoard: function () {
        var x, y, color, egg;

        this.drawLine();

        for (var i = 0; i < this.state.egg_pos.length; ++i) {
            egg = this.state.egg_pos[i];
            x = egg.x_pos;
            y = egg.y_pos;
            color = egg.color;
            if (egg.alive) {
                this.drawEgg(x, y, color);
            }
        }

        if (!this.state.is_turn_end) {
            setTimeout(this.updateBoard, 1000 / this.state.frame);
        }
    },
    funcSleep: function(num) {
        var now = new Date();

        var stop = now.getTime() + num;

        while(true){

            now = new Date();

            if(now.getTime() > stop) return;

        }
    },
    render: function () {
        return (
            <section id="center">
                <h3>
                    <span>&#9899; </span>
                    {this.state.players.map((name, i) => {
                        if (i >= this.state.players.length - 1) {
                            return (<span key={i}>{name}</span>);
                        }
                        else {
                            return (<span key={i}>{name} vs </span>);
                        }
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

Egg.prototype.addForce = function (x_dir, y_dir, force) {
    this.x_dir = x_dir;
    this.y_dir = y_dir;
    this.speed = force;
    return true;
};

Egg.prototype.isMeet = function (x, y, rad, board) {
    var radius = rad;
    var board_size = board;
    var distance = Math.sqrt((this.x_pos - x) * (this.x_pos - x) + (this.y_pos - y) * (this.y_pos - y));

    return (distance <= radius * 2) && this.alive && x >= 0 && x <= board_size && y >= 0 && y <= board_size;
};

function decodeData(str_data) {
    var decoded_str = str_data.replace(/&#39;/g, '\"');
    var match_data = jQuery.parseJSON(decoded_str);
    console.log(match_data)
    var players = match_data.players;
    var type = match_data.type;
    var _id = match_data._id

    React.render(<Game players={ players } _id={ _id } type={ type }/>, document.getElementById('Game'));
}