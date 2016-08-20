#-*-coding:utf-8-*-
from gameLogic.othello.othellGameParser import OthelloParser
import random

class MyOthelloParser(OthelloParser):
    def parsingGameData(self, decoding_data):
        msg = decoding_data['msg']
        msg_type = decoding_data['msg_type']
        game_data = decoding_data['game_data']

        parsing_data = {}

        if msg_type == 'on_turn':
            #on_turn 시에 주어지는 부가 정보 목록이다.
            board = game_data['board']
            black = game_data['black']
            white = game_data['white']
            self.none = game_data['none']

            # 이제 이 부가정보들을 가지고 논리를 진행하도록 하자.
            validMoves = self.getValidMoves(board, black, white, self.pid)
            if validMoves != []:
                randomXY = validMoves[random.randrange(0, len(validMoves))]
                parsing_data = {'x': randomXY[0], 'y': randomXY[1]}
                #                print randomXY,self.pid
            else:
                parsing_data = {'x': -1, 'y': -1}

            send_msg = self.makeSendMsg(msg_type, parsing_data)
            return send_msg

        elif msg_type == 'finish':
            send_msg = self.makeSendMsg(msg_type, parsing_data)
            return send_msg

        elif msg_type == 'init':
            parsing_data = {'response': 'OK'}
            send_msg = self.makeSendMsg(msg_type, parsing_data)
            return send_msg
