#-*-coding:utf-8-*-
import random

from game.othello import OthelloAIParser2


class MyOthelloParser2(OthelloAIParser2):
    def on_turn_phase(self):
        '''
        input:
        self.game_data['board'] : 8x8 board infomation
        self.game_data['black'] : black player's pid
        self.game_data['white'] : white player's pid
        :return: {'x': int, 'y' : int}를 make_send_msg를 사용하여 묶은 후 반환
        '''
        board = self.game_data['board']
        black = self.game_data['black']
        white = self.game_data['white']

        print black, white, board

        # 이제 이 부가정보들을 가지고 논리를 진행하도록 하자.
        valid_moves = self.get_valid_moves(board, black, white, self.pid)
        if valid_moves != []:
            random_x_y = valid_moves[random.randrange(0, len(valid_moves))]
            parsing_data = {'x': random_x_y[0], 'y': random_x_y[1]}
            #                print randomXY,self.pid
        else:
            parsing_data = {'x': -1, 'y': -1}

        send_msg = self.make_send_msg(self.msg_type, parsing_data)
        return send_msg