class Phase(object):
	def __init__(self, logicServer, messageType):
		self._logicServer = logicServer
		self.messageType = messageType
		self.nofityMessageType = 'notify_' + messageType
		pass

	def onStart(self):
		pass

	def doAction(self,pid, args):
		return True

	def onEnd(self):
		pass

	def changePhase(self, index):
		self._logicServer.changePhase(index)

	def changeTurn(self, index = None):
		self._logicServer.changeTurn(index)

	def nowTurn(self):
		return self._logicServer.nowTurn()

	def request(self, pid, JSON):
		self._logicServer.request(pid, self.messageType, JSON)

	def requestAll(self, JSON):
		self._logicServer.requestAll(self.messageType, JSON)

	def end(self, isValidEnd, resultList):
		self._logicServer.end(isValidEnd, resultList)
		
	def getSharedDict(self):
		return self._logicServer.getSharedDict()

	def getPlayerList(self):
		return self._logicServer.getPlayerList()
	
	def notify(self, JSON):
		self._logicServer.notify(self.nofityMessageType, JSON)