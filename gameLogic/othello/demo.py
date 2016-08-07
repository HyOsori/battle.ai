import sys
from othelloServer import OthelloTurnGameLogic
import json
import logging
logging.basicConfig(level = logging.DEBUG)
import random

def showTable(board):
    for y in range(8):
        for x in range(8):
            sys.stdout.write(board[x][y]+' ')
        print ''
    print '#'*39

class SampleRoom():
	def __init__(self, players):
		self.gamelogic = OthelloTurnGameLogic(self)
		self.playerList = [x.pid for x in players]
		self.playerDict = dict(zip(self.playerList, players))
	def start(self):
		self.gamelogic.onStart(self.playerList)
	def request(self, pid, messageType, JSON):
		self.gamelogic.onAction(pid, self.playerDict[pid].request(messageType, JSON))
	def onEnd(self, isValid, result):
		logging.debug('isValid is ' + str(isValid) + ', result is ' + str(result))
		pass

class AI(object):
	def __init__(self, pid):
		self.pid = pid
	def request(self, messageType, JSON):
		pass

class RandomAI(AI):
    def __init__(self, pid):
        super(RandomAI,self).__init__(pid)

    def request(self, messageType, JSON):
        requsetInfo = json.loads(JSON)

        self.board = requsetInfo['board']
        self.black = requsetInfo['black']
        self.white = requsetInfo['white']
        self.none = requsetInfo['none']
        showTable(self.board)
        if messageType == 'on_turn':
            validMoves = self.getValidMoves(self.pid)
            if validMoves != []:
                randomXY = validMoves[random.randrange(0,len(validMoves))]
            else:
                return json.dumps({'x':-1,'y':-1})
            return json.dumps({'x':randomXY[0],'y':randomXY[1]})

        elif messageType == 'finish':
            return json.dumps({'response':'OK'})

    def isOnBoard(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def isValidMove(self, tile, xstart, ystart):
        self.board[xstart][ystart] = tile
        if tile == self.black:
            otherTile = self.white
        else:
            otherTile = self.black

        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if self.isOnBoard(x, y) and self.board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while self.board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        break
                if not self.isOnBoard(x, y):
                    continue
                if self.board[x][y] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        self.board[xstart][ystart] = self.none
        if len(tilesToFlip) == 0:
            return False
        return tilesToFlip

    def getValidMoves(self, tile):
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.isValidMove(tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

if __name__ == '__main__':
    game = SampleRoom([RandomAI('----'), RandomAI('****')])
    game.start()

