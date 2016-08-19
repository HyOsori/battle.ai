import sys
sys.path.insert(0,'../')
from baseClass import gameDataParser

import random

class OthelloParser(gameDataParser):
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