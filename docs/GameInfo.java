public class GameInfo {
	/* 마이 페이지에서 볼 내 게임에 대한 정보 */
	/*
	* title : 게임 결과로 얻은 칭호
	* file[] : 한 게임에 등록해놓은 여러 파일들
	*/

	private String game_id;
	private String title;
	private int win;
	private int lose;
	private int draw;

	// file
	private String primary_file_id; 
	private file[] files;
}
