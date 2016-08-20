
#-*-coding:utf-8-*-
#인터페이스 로써 작동하도록 하자

class GameDataParser:
    def initParser(self,client,username):
        self._client = client
        self.pid = username

    #game_data 로는 room에서 보낸 json이 loads된 상태의 dict 자료형이 반환된다.
    #dict자료형에 대한 정보는 문서를 참조하며, 그 dict의 정보를 활용하여 logic을 실행 시킨다.
    #그리고 반환형에 맞춰서 정보를 조작한후 리턴한다.

    #고로 이 부분이 사용자가 코딩할 부분!

    def parsingGameData(self,decoding_data):
        pass

    def makeSendMsg(self, msg_type, game_data):
        send_msg = {"msg": "game_data"}
        send_msg["msg_type"] = msg_type
        send_msg["game_data"] = game_data
        return send_msg