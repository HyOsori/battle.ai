class Phase(object):
	def __init__(self, logicServer, messageType):
		self._logicServer = logicServer
		self.messageType = messageType
		self.nofityMessageType = 'notify_' + messageType
		pass

	def onStart(self):
		pass

	def doAction(self,pid, dictData):
		return True

	def onEnd(self):
		pass

	def changePhase(self, index):
		self._logicServer.changePhase(index)

	def changeTurn(self, index = None):
		self._logicServer.changeTurn(index)

	def nowTurn(self):
		return self._logicServer.nowTurn()

	def request(self, pid, dictData):
		self._logicServer.request(pid, self.messageType, dictData)

	def requestAll(self, dictData):
		self._logicServer.requestAll(self.messageType, dictData)

	def end(self, isValidEnd, resultList=None):
		self._logicServer.end(isValidEnd, resultList)
		
	def getSharedDict(self):
		return self._logicServer.getSharedDict()

	def getPlayerList(self):
		return self._logicServer.getPlayerList()

	def setPlayerResult(self, pid, result):
		self._logicServer.setPlayerResult(pid, result)

	def setAllPlayerResult(self, result):
		self._logicServer.setAllPlayerResult(result)

	def getPlayerResult(self, pid):
		return self._logicServer.getPlayerResult(pid)
	
	def notify(self, dictData):
		self._logicServer.notify(self.nofityMessageType, dictData)