import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic
from gameLogic.baseClass.Phase import Phase
#import json
import logging
logging.basicConfig(level=logging.DEBUG)

'''
ShardDict Key

PHASE_ONTURN -> 'on_turn'->
PHASE_END    -> 'finish'->
board

'''

class OthelloOnTurnPhase(Phase):
    def __init__(self, logicServer, messageType):
        super(OthelloOnTurnPhase, self).__init__(logicServer,messageType)

    def onStart(self):
        super(OthelloOnTurnPhase,self).onStart()
        logging.debug('##OthelloOnTurnPhase Start')
        self.playerList = self.getPlayerList()
        shardDict = self.getSharedDict()

        self.black = self.playerList[0]
        self.white = self.playerList[1]
        self.none = 'NONE'
        self.board = shardDict['board']
        self.nextPhase = shardDict['PHASE_END']

        self.changeTurn(0)
        self.requestAndSendBoard()

    def doAction(self,pid , dictData): # need args -> [turn , x , y]
        super(OthelloOnTurnPhase,self).doAction(pid,dictData)
        logging.debug('OthelloOnTurnPhase doAction from ' + pid + ' Processing...')
        if pid != self.nowTurn():
            result = dict(zip(self.playerList, ['win'] * len(self.playerList)))
            result[pid] = 'lose'
            logging.error(pid + ' is not equal to current turn player;' + self.nowTurn())
            self.end(False, result)
            return

        try:
            actionInfo = dictData
            x = int(actionInfo['x'])
            y = int(actionInfo['y'])

            if self.isValidMove(pid,x,y) == False:
                result = dict(zip(self.playerList, ['win'] * len(self.playerList)))
                result[pid] = 'lose'
                logging.error(pid+' invalid Move')
                self.end(False, result)
                return

            if pid == self.white:
                oppsite = self.black
            else:
                oppsite = self.white

            validMoves = self.getValidMoves(pid)

            if validMoves != []:
                self.makeMove(pid,x,y) # change board
                self.notifyBoard(pid, x, y) # notify change board


            if self.isGameEnd():
                self.changePhase(self.nextPhase)
                return

            if self.getValidMoves(oppsite) != []:
                self.changeTurn()


            self.requestAndSendBoard()

        except Exception, e:
            logging.debug(e)
            logging.error(pid+' causes Exception during OthelloOnTurnPhase')
            result = dict(zip(self.playerList, ['win'] * len(self.playerList)))
            result[pid] = 'lose'
            self.end(False, result)

    def isValidMove(self, tile, xstart, ystart):
        if self.board[xstart][ystart] != self.none or not self.isOnBoard(xstart, ystart):
            return False

        self.board[xstart][ystart] = tile  # temporarily set the tile on the board.

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

    def isOnBoard(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def getValidMoves(self, tile):
        validMoves = []

        for x in range(8):
            for y in range(8):
                if self.isValidMove(tile, x, y) != False:
                    validMoves.append([x, y])
        return validMoves

    def makeMove(self, tile, xstart, ystart):
        tilesToFlip = self.isValidMove(tile, xstart, ystart)

        if tilesToFlip == False:
            return False

        self.board[xstart][ystart] = tile
        for x, y in tilesToFlip:
            self.board[x][y] = tile
        return True

    def onEnd(self):
        super(OthelloOnTurnPhase,self).onEnd()
        logging.debug('##OthelloOnTurnPhase End')

    def isGameEnd(self):
        bCount = 0
        wCount = 0

        for x in range(8):
            for y in range(8):
                if self.board[x][y] == self.black:
                    bCount = bCount+1
                elif self.board[x][y] == self.white:
                    wCount = wCount+1

        if (bCount == 0) or (wCount == 0) or (bCount+wCount == 64):
            return True
        return False

    def changeBoardtoInteger(self):
        intBoard = [[0 for col in range(8)] for row in range(8)]
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == self.none:
                    intBoard[x][y] = 0
                elif self.board[x][y] == self.black:
                    intBoard[x][y] = 1
                elif self.board[x][y] == self.white:
                    intBoard[x][y] = 2

        return intBoard

    def notifyBoard(self,pid,x,y):
        intBoard = self.changeBoardtoInteger()
        notifyDict = {
            'board' : intBoard,
            'x' : x,
            'y' : y,
            'black' : self.black,
            'white' : self.white,
            'now_turn' : pid
        }

        self.notify(notifyDict)

    def requestAndSendBoard(self):
        logging.debug('Request ' + self.nowTurn() + '\'s decision')
        info_dict = {
            'board': self.board,
            'black': self.black,
            'white': self.white,
            'none': self.none
        }
        self.request(self.nowTurn(),info_dict)

class OthelloEndPhase(Phase):
    def __init__(self, logicServer,messageType):
        super(OthelloEndPhase,self).__init__(logicServer,messageType)

    def onStart(self):
        super(OthelloEndPhase, self).onStart()
        logging.debug('OthelloEndPhase Start')
        self.playerList = self.getPlayerList()
        shardDict = self.getSharedDict()
        self.black = self.playerList[0]
        self.white = self.playerList[1]

        self.cntPlayer = 2
        self.board = shardDict['board']

        self.sendGameOver()

    def getScoreOfBoard(self):
        blackScore = 0
        whiteScore = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == self.black:
                    blackScore += 1
                if self.board[x][y] == self.white:
                    whiteScore += 1

        resultDict = {
            'black_score' : blackScore,
            'white_score' : whiteScore
        }

        if blackScore > whiteScore:
            resultDict['winner'] = self.black
        elif whiteScore > blackScore:
            resultDict['winner'] = self.white
        else:
            resultDict['draw'] = True

        return resultDict

    def doAction(self, pid, dictData):
        # args is not using
        super(OthelloEndPhase, self).doAction(pid,dictData)
        try:
#            args = dictData
#            response = args['response']
#            if response != 'OK':
#                self.setPlayerResult(pid,'error')

            self.cntPlayer -= 1

            if self.cntPlayer == 0:
                resultDict = self.getScoreOfBoard()
                self.notifyWinner(resultDict)
                logging.error(pid + ' **************************')
                self.end(True)
                return

            self.changeTurn()
            self.sendGameOver()

        except Exception, e:
            logging.debug(e)
            logging.error(pid + ' causes Exception during result')
            result = dict(zip(self.playerList, ['win'] * len(self.playerList)))
            result[pid] = 'lose'
            self.end(False, result)

    def onEnd(self):
        super(OthelloEndPhase, self).onEnd()
        logging.debug('===ResultPhase End===')

    def notifyWinner(self,winnerDict):
        notifyDict = winnerDict

        self.notify(notifyDict)

    def sendGameOver(self):
        logging.debug('Send gameover message to ' + self.nowTurn())
        self.request( self.nowTurn() ,{})

#######################################
#######################################

##messageType -> onTurn = {x,y}
##            -> finish = {response}
##
class OthelloTurnGameLogic(TurnGameLogic):
    def __init__(self, gameServer):
        super(OthelloTurnGameLogic,self).__init__(gameServer)
        self.none = "NONE"
        self.board = [[self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none]]


        logging.debug('Othello Logic Init')
        logging.debug('LogicServer init finish')

    def onStart(self, playerList):
        super(OthelloTurnGameLogic,self).onStart(playerList)
        self.black = playerList[0]  # first player's name
        self.white = playerList[1]  # second player's name
        self.board = [[self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.white, self.black, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.black, self.white, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none]]

        shardDict = self.getSharedDict()
        shardDict['board'] = self.board
        logging.debug('Othello Phase Init')
        onTurnPhase = OthelloOnTurnPhase(self, 'on_turn')
        endPhase = OthelloEndPhase(self, 'finish')
        shardDict['PHASE_ONTURN'] = self.appendPhase(onTurnPhase)
        shardDict['PHASE_END'] = self.appendPhase(endPhase)

        logging.debug('Phase init finish')

        logging.debug('Othello Game Start')
        self.changeTurn(0)
        self.changePhase(0)

    def onError(self,pid):
        super(OthelloTurnGameLogic,self).onError(pid)