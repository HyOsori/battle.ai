import sys
sys.path.insert(0, '../')
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic
from gameLogic.baseClass.Phase import Phase
import logging
logging.basicConfig(level=logging.DEBUG)


class InitPhase(Phase):
	def __init__(self, logicServer, messageType):
		super(InitPhase, self).__init__(logicServer, messageType)

	def onStart(self):
		logging.debug('===InitPhase Start===')
		sd = self.getSharedDict()
		self.nextPhase = sd['PHASE_GAMELOOP']
		self.cntPlayer = len(self.getPlayerList())
		self.minCnt = sd['minCnt']
		self.maxCnt = sd['maxCnt']
		self.goal = sd['goal']

		self.sendConfig()

	def doAction(self, pid, dictData):
		logging.debug('Receive response from ' + pid + '. Processing...')
		if pid != self.nowTurn():
			logging.error(pid + ' is not equal to current turn player;' + self.nowTurn())
			self.setPlayerResult(pid, 'error')
			self.end(False)
			return

		try:
			args = dictData
			response = args['response']
			if response == 'OK':
				self.cntPlayer -= 1
				if self.cntPlayer == 0:
					logging.debug('All users responsed OK. Go to the next phase...')
					self.setAllPlayerResult('win')
					self.changePhase(self.nextPhase)
					return

				self.changeTurn()
				self.sendConfig()
				return

			else:
				logging.error(pid + ' responsed incorrect message;' + response)
				self.setPlayerResult(pid, 'error')
				self.end(False)
				return

		except Exception, e:
			logging.debug(e)
			logging.error(pid + ' causes Exception during init')
			self.setPlayerResult(pid, 'error')
			self.end(False)
			return

	def onEnd(self):
		logging.debug('===InitPhase End===')

	def sendConfig(self):
		logging.debug('Send configure data to ' + self.nowTurn())
		self.request(self.nowTurn(),
			 {
			'min': self.minCnt,
			'max': self.maxCnt,
			'finish': self.goal
			}
		)


class GameLoopPhase(Phase):
	def __init__(self, logicServer, messageType):
		super(GameLoopPhase, self).__init__(logicServer, messageType)

	def onStart(self):
		logging.debug('===GameLoopPhase Start===')
		sd = self.getSharedDict()
		self.minCnt = sd['minCnt']
		self.maxCnt = sd['maxCnt']
		self.goal = sd['goal']
		self.nextPhase = sd['PHASE_RESULT']
		self.cnt = 1
		self.changeTurn(0)
		logging.debug('Game start! First number is ' + str(self.cnt) + '.')
		self.requestDecision()

	def doAction(self, pid, dictData):
		logging.debug('Receive response from ' + pid + '. Processing...')
		if pid != self.nowTurn():
			self.setPlayerResult(pid, 'lose')
			logging.error(pid + ' is not equal to current turn player;' + self.nowTurn())
			self.end(False)
			return

		try:
			args = dictData
			num = int(args['num'])
			if num < self.minCnt or num > self.maxCnt:
				self.setPlayerResult(pid, 'lose')
				logging.error(pid + ' responsed invalid range number')
				self.end(False)
				return

			self.notify({
				'pid': pid,
				'num': num
			})

			if self.cnt + num > self.goal:
				self.setPlayerResult(pid, 'lose')
				logging.debug('Game is over. ' + pid + ' said ' +
					str(self.goal) + '. Go to the next phase...')
				self.changePhase(self.nextPhase)
				return
			self.cnt += num
			logging.debug(pid + ' counted ' + str(num) +
						'. So next player start from ' + str(self.cnt))
			self.changeTurn()
			self.requestDecision()
			return

		except Exception, e:
			logging.debug(e)
			logging.error(pid + ' causes Exception during gameloop')
			self.setPlayerResult(pid, 'lose')
			self.end(False)
			return

	def onEnd(self):
		logging.debug('===GameLoopPhase End===')

	def requestDecision(self):
		logging.debug('Request ' + self.nowTurn() + '\'s decision')
		self.request(self.nowTurn(),
			{
			'start': self.cnt
			}
		)


class ResultPhase(Phase):
	def __init__(self, logicServer, messageType):
		super(ResultPhase, self).__init__(logicServer, messageType)

	def onStart(self):
		logging.debug('===ResultPhase Start===')
		self.cntPlayer = len(self.getPlayerList())
		self.sendGameOver()

	def doAction(self, pid, dictData):
		try:
			args = dictData
			response = args['response']
			if response != 'OK':
				self.setPlayerResult(pid, 'error')

			self.cntPlayer -= 1
			if self.cntPlayer == 0:
				logging.debug('All users know that game is over. end the game...')
				self.end(True)
				return

			self.changeTurn()
			self.sendGameOver()
			return
		except Exception, e:
			logging.debug(e)
			logging.error(pid + ' causes Exception during result')
			self.setPlayerResult(pid, 'error')
			self.end(False)
			return

	def onEnd(self):
		logging.debug('=======ResultPhase End======')

	def sendGameOver(self):
		logging.debug('Send gameover message to ' + self.nowTurn())
		self.request(self.nowTurn(), {})


class BaskinServer(TurnGameLogic):
	def __init__(self, room):
		super(BaskinServer, self).__init__(room)
		sd = self.getSharedDict()
		sd['goal'] = 31
		sd['minCnt'] = 1
		sd['maxCnt'] = 3
		sd['result'] = {}
		logging.debug('===BaskinRobbins game initialization===')
		logging.debug('finish number is ' + str(sd['goal']) + ', min is ' + str(
			sd['minCnt']) + ', max is ' + str(sd['maxCnt']))

		logging.debug('===BaskinRobbins phase initialization===')
		initPhase = InitPhase(self, 'init')
		gameloopPhase = GameLoopPhase(self, 'gameloop')
		resultPhase = ResultPhase(self, 'finish')
		sd['PHASE_INIT'] = self.appendPhase(initPhase)
		sd['PHASE_GAMELOOP'] = self.appendPhase(gameloopPhase)
		sd['PHASE_RESULT'] = self.appendPhase(resultPhase)
		logging.debug('===BaskinRobbins phase initialization complete===')
		logging.debug('===BaskinRobbins game initialization complete===')

	def onStart(self, playerList):
		super(BaskinServer, self).onStart(playerList)
		logging.debug('===BaskinRobbins game start===')
		self.changeTurn(0)
		self.changePhase(0)

	def onError(self, pid):
		super(BaskinServer, self).onError(pid)
		self.setPlayerResult(pid, 'error')
		self.end(False)
		
