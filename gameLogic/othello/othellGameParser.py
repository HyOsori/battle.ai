z#-*-coding:utf-8-*-
import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.gameDataParser import GameDataParser

import random

#msg_type -> on_turn 과 finish를 처리해야함
#on_turn 은 보드의 정보와 black, white에 대한 정보가 dict로 날라옴, 이를 적절히 처리
#하여 자신이 둘 x,y좌표를 보내면 됨
3
#finish메시지에선 별다른 처리가 필요없을 것 같음 아직

#on_turn 의 key = board, black, white, none -> board는 8*8짜리 2차원 배열이며
#board는 각각 black, white, none 의 정보로 구성되어있으며
#board에서 자신이 선공이라면 자신의 pid가 black, 아니라면 white

#주어진 보드에서 black, white가 둘 수 있는 리스트를 받아올수 있다.(getValidMoves를 사용하면)
class OthelloParser(GameDataParser):
    def __init__(self):
        self.none = 'None'

    def parsingGameData(self,decoding_data):
        pass

    def isOnBoard(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def isValidMove(self,board,black,white, tile, xstart, ystart):
        if board[xstart][ystart] != self.none or not self.isOnBoard(xstart, ystart):
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
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        break
                if not self.isOnBoard(x, y):
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

    def getValidMoves(self,board,black,white, tile):
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.isValidMove(board,black,white,tile, x, y) != False:
                    validMoves.append([x, y])

        return validMoves

    def showTable(self,board):
        for y in range(8):
            for x in range(8):
                sys.stdout.write(board[x][y] + ' ')
            print ''
        print '#' * 39