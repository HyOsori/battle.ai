RESTFUL API

/* 메인 페이지 */
회원 가입 POST /auth/signup
로그   인 POST /auth/signin

/* 마이 페이지 */
랜더링 해줄거 GET /aifile
파일 추가하기 POST /aifile
파일 삭제하기 DELETE /aifile


WEB SOCKET PROTOCOL

protocol : {msg, msg_type, data}

/* 로비 페이지 */
--------Log--------

Get Log 시 log data 초기화 
	Client -> request_game_log {"gamelog", "init", null}
	Server -> response_game_log {"gamelog", "init", data}  data = gamelog List[];

Game Log 추가시 notify
	Server -> notify_client_game_log {"gamelog", "add", data}  data = new gamelog;

--------Chat--------

Chat 사용자가 추가시 notify를 요청
	Client -> notify_server_new_chat {"chat", "send", data} data = new chat;

Chat notify
	Server -> notify_client_new_chat {"chat", "receive", data} data = new chat;

Get AIList 시 List data 초기화
	Client -> request_ailist {"ailist", "init", null}
	Server -> response_ailist {"ailist", "init", data}  data = aifile List[];

--------AIList--------


ailist 사용자가 추가시 notify
	Server -> notify_client_add_ailist {"ailist", "add", data} data = new aifile;

ailist 받았을 시 notify
	Server -> notify_client_del_ailist {"ailist", "delete", data} data = new aifile;

--------match--------

match 버튼 클릭 했다
	Client -> request_match {"나중에 ㅈ거어리", "match", data} data = playerlist;
	Server -> response_match {"나중에 ㅈ겅", "match", data}  data = {"response": boolean};


/* 게임 페이지 */



