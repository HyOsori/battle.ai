public class GameLog {
	/* 게임 종료시 남는 Log */

	/*
	* players : 1:1 이라 가정하면 [player1, player2];
	* game_result : 게임 종료 상태(draw, win(who is winner)), 추가 정보 
	*/
	private Player[] players;
	private GameResult game_result;
	private GameMessage[] game_message;
}