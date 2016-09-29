#-*-coding:utf-8-*-
from gameLogic.othello.OthelloAIParser import OthelloAIParser
import random

class MyOthelloParser(OthelloAIParser):
    def parsing_data(self, decoding_data):
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
            valid_moves = self.get_valid_moves(board, black, white, self.pid)
            if valid_moves != []:
                random_x_y = valid_moves[random.randrange(0, len(valid_moves))]
                parsing_data = {'x': random_x_y[0], 'y': random_x_y[1]}
                #                print randomXY,self.pid
            else:
                parsing_data = {'x': -1, 'y': -1}

            send_msg = self.make_send_msg(msg_type, parsing_data)
            return send_msg

        elif msg_type == 'finish':
            parsing_data['response'] = 'OK'
            send_msg = self.make_send_msg(msg_type, parsing_data)
            return send_msg

        elif msg_type == 'init':
            parsing_data['response'] = 'OK'
            send_msg = self.make_send_msg(msg_type, parsing_data)
            return send_msg
