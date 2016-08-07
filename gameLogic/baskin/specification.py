'''
BaskinRobbins게임의 진행 단계
1. InitPhase
 메시지타입 : "init"
서버에서
{
	min : 한번에 count할수 있는 최소값(int),
	max : 한번에 count할수 있는 최대값(int),
	finish : 이 숫자를 부른 player가 패배(int)
}
형식으로 JSON을 한명씩 보내게 되며
플레이어가 이를 받았을 때
{
	response : "OK"
}
를 보내면 다음 플레이어에게 같은 내용을 전달한다.
모든 플레이어가 OK를 보내오면 다음 페이즈로 진행
2. GameLoopPhase
 메시지타입 : "gameloop"
서버에서
{
	start : 이 숫자부터 부를 차례(int)
}
형식으로 JSON을 턴 순서대로 보내게 되며
플레이어가 이를 받았을 때
{
	num : 현재 불러야 하는 시작 숫자에서 몇개나 부를지(int). min <= num <= max이어야 함.
}
를 보내면 서버에서 게임 종료여부, 반칙여부를 판단하고 정상적인 경우 다음 플레이어에게 같은 형식으로 전달한다.
finish값을 부르는 플레이어가 있는 경우 다음 페이즈로 진행

매 턴마다 모든 플레이어에게 notify를 하게 되는데 그 때형식은
메시지타입 : "notify_gameloop"
{
	pid : 플레이어이름
	num : 현재 불러야 하는 시작 숫자에서 몇개나 부를지(int). min <= num <= max이어야 함.
}

3. ResultPhase
 메시지타입 : "finish"
서버에서
{
} //아무 값도 없는 빈 JSON
형식으로 JSON을 턴 순서대로 보내게 되며
플레이어가 이를 받았을 때
{
	response : "OK"
}
를 보내야 하며 모두 OK를 보내오면 종료
'''