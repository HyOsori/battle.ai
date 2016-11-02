#-*-coding:utf-8-*-
import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.AIParser import AIParser

import random

#msg_type -> on_turn 과 finish를 처리해야함
#on_turn 은 보드의 정보와 black, white에 대한 정보가 dict로 날라옴, 이를 적절히 처리
#하여 자신이 둘 x,y좌표를 보내면 됨
#finish메시지에선 별다른 처리가 필요없을 것 같음 아직

#on_turn 의 key = board, black, white, none -> board는 8*8짜리 2차원 배열이며
#board는 각각 black, white, none 의 정보로 구성되어있으며
#board에서 자신이 선공이라면 자신의 pid가 black, 아니라면 white

#주어진 보드에서 black, white가 둘 수 있는 리스트를 받아올수 있다.(getValidMoves를 사용하면)
class OthelloAIParser2(AIParser):
    def __init__(self):
        self.none = 'NONE'

    def parsing_data(self, decoding_data):
        super(OthelloAIParser2, self).parsing_data(decoding_data)
        if self.msg_type == 'on_turn':
            return self.on_turn_phase()

    def on_turn_phase(self):
        '''
        이것을 구현하기만 하면된다!
        on_turn Phase에 해당하는 logic을 작성한다.
        :return: make_send_msg를 사용해서 json으로 묶은 것을 return 해주어야 한다.
        '''
        pass

    def is_on_board(self, x, y):
        '''

        :param x:
        :param y:
        :return: boolean
        '''
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def is_valid_move(self, board, black, white, tile, xstart, ystart):
        if board[xstart][ystart] != self.none or not self.is_on_board(xstart, ystart):
            return False

        board[xstart][ystart] = tile
        if tile == black:
            otherTile = white
        else:
            otherTile = black

        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if self.is_on_board(x, y) and board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not self.is_on_board(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.is_on_board(x, y):
                        break
                if not self.is_on_board(x, y):
                    continue
                if board[x][y] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        board[xstart][ystart] = self.none
        if len(tilesToFlip) == 0:
            return False
        return tilesToFlip

    def get_valid_moves(self, board, black, white, tile):
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.is_valid_move(board, black, white, tile, x, y) != False:
                    validMoves.append([x, y])

        return validMoves

    def show_table(self, board):
        for y in range(8):
            for x in range(8):
                sys.stdout.write(board[x][y] + ' ')
            print ''
        print '#' * 39
