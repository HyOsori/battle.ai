import abc

class TurnGameLogic(object):
	__metaclass__ = abc.ABCMeta
	def __init__(self, room):
		self._room = room
		self._phaseList = []
		self._currentPhase = None
		self._sharedDict = {}

	def onStart(self, playerList):
		self._playerList = playerList
		self._turnNum = -1
		self.changeTurn()

	def onAction(self,pid,JSON):
		return self._currentPhase.doAction(pid, JSON)

	@abc.abstractmethod
	def onError(self, pid):
		pass

	def changePhase(self, index):
		if self._currentPhase != None:
			self._currentPhase.onEnd()
		self._currentPhase = self._phaseList[index]
		self._messageType = self._currentPhase.messageType
		self._currentPhase.onStart()

	def changeTurn(self, index = None):
		if index != None:
			self._turnNum = index
		else:
			self._turnNum = self._turnNum + 1

	def nowTurn(self):
		length = len(self._playerList)
		return self._playerList[self._turnNum%length]

	def requestAll(self, messageType, JSON):
		for pid in self._playerList:
			self.request(pid, messageType, JSON)

	def request(self, pid, messageType, JSON):
		self._room.request(pid, messageType, JSON)

	def end(self, isValidEnd, resultList):
		self._room.onEnd(isValidEnd, resultList)

	def appendPhase(self, phase):
		self._phaseList.append(phase)
		return len(self._phaseList)-1
		
	def getSharedDict(self):
		return self._sharedDict

	def getPlayerList(self):
		return self._playerList
