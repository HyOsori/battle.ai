from gameLogic.baseClass.TurnGameLogic import TurnGameLogic

class dummy_GameLogic(TurnGameLogic):

    def __init__(self, room, args):
        self.room = room
        self.phaseList = []
        self.messageList = []
        self.currentPhase = None


    def onStart(self, args):
        self.playerList = args
        self.turnNum = -1
        self.changeTurn()

    def onAction(self, pid, args):
        self.currentPhase.doAction(args)

    def onEnd(self):
        pass

    def onError(self, pid):
        pass

    def changePhase(self, index):
        if self.currentPhase != None:
            self.currentPhase.onEnd()
        self.currentPhase = self.phaseList[index]
        self.currentPhase.onStart()
        self.message = self.messageList[index]

    def changeTurn(self):
        self.turnNum = self.turnNum + 1

    def changeTurn(self, index):
        self.turnNum = index

    def nowTurn(self):
        length = len(self.playerList)
        return self.playerList[self.turnNum % length]

    def requset(self, pid, messageType, JSON):
        self.room.requset(pid, messageType, JSON)