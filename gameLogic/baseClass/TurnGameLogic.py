import abc

class TurnGameLogic:
    __metaclass__ = abc.ABCMeta
    def __init__(self, GameServer):
        self.game_server = GameServer
        self.phaseList = []
        self.messageList = []
        self.currentPhase = None

    def onStart(self, args):
        self.playerList = args
        self.turnNum = -1
        self.changeTurn()

    def onAction(self,pid,args):
        self.currentPhase.doAction(args)

    @abc.abstractmethod
    def onEnd(self):
        pass

    @abc.abstractmethod
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

    # def changeTurn(self, index):
    #     self.turnNum = index

    def nowTurn(self):
        length = len(self.playerList)
        return self.playerList[self.turnNum%length]

    def request(self, pid, messageType, JSON):
        self.game_server.request(pid, messageType, JSON)