import sys
sys.path.insert(0, '../')
from game.base.TurnGameLogic import TurnGameLogic
from game.base.Phase import Phase
import logging
logging.basicConfig(level=logging.DEBUG)


class InitPhase(Phase):
	def __init__(self, logic_server, messageType):
		super(InitPhase, self).__init__(logic_server, messageType)

	def on_start(self):
		logging.debug('===InitPhase Start===')
		sd = self.get_shared_dict()
		self.nextPhase = sd['PHASE_GAMELOOP']
		self.cntPlayer = len(self.get_player_list())
		self.minCnt = sd['minCnt']
		self.maxCnt = sd['maxCnt']
		self.goal = sd['goal']

		self.sendConfig()

	def do_action(self, pid, dict_data):
		logging.debug('Receive response from ' + pid + '. Processing...')
		if pid != self.now_turn():
			logging.error(pid + ' is not equal to current turn player;' + self.now_turn())
			self.set_player_result(pid, 'error')
			self.end(False)
			return

		try:
			args = dict_data
			response = args['response']
			if response == 'OK':
				self.cntPlayer -= 1
				if self.cntPlayer == 0:
					logging.debug('All users responsed OK. Go to the next phase...')
					self.set_all_player_result('win')
					self.change_phase(self.nextPhase)
					return

				self.change_turn()
				self.sendConfig()
				return

			else:
				logging.error(pid + ' responsed incorrect message;' + response)
				self.set_player_result(pid, 'error')
				self.end(False)
				return

		except Exception, e:
			logging.debug(e)
			logging.error(pid + ' causes Exception during init')
			self.set_player_result(pid, 'error')
			self.end(False)
			return

	def on_end(self):
		logging.debug('===InitPhase End===')

	def sendConfig(self):
		logging.debug('Send configure data to ' + self.now_turn())
		self.request(self.now_turn(),
					 {
			'min': self.minCnt,
			'max': self.maxCnt,
			'finish': self.goal
			}
					 )


class GameLoopPhase(Phase):
	def __init__(self, logic_server, messageType):
		super(GameLoopPhase, self).__init__(logic_server, messageType)

	def on_start(self):
		logging.debug('===GameLoopPhase Start===')
		sd = self.get_shared_dict()
		self.minCnt = sd['minCnt']
		self.maxCnt = sd['maxCnt']
		self.goal = sd['goal']
		self.nextPhase = sd['PHASE_RESULT']
		self.cnt = 1
		self.change_turn(0)
		logging.debug('Game start! First number is ' + str(self.cnt) + '.')
		self.requestDecision()

	def do_action(self, pid, dict_data):
		logging.debug('Receive response from ' + pid + '. Processing...')
		if pid != self.now_turn():
			self.set_player_result(pid, 'lose')
			logging.error(pid + ' is not equal to current turn player;' + self.now_turn())
			self.end(False)
			return

		try:
			args = dict_data
			num = int(args['num'])
			if num < self.minCnt or num > self.maxCnt:
				self.set_player_result(pid, 'lose')
				logging.error(pid + ' responsed invalid range number')
				self.end(False)
				return

			self.notify({
				'pid': pid,
				'num': num
			})

			if self.cnt + num > self.goal:
				self.set_player_result(pid, 'lose')
				logging.debug('Game is over. ' + pid + ' said ' +
					str(self.goal) + '. Go to the next phase...')
				self.change_phase(self.nextPhase)
				return
			self.cnt += num
			logging.debug(pid + ' counted ' + str(num) +
						'. So next player start from ' + str(self.cnt))
			self.change_turn()
			self.requestDecision()
			return

		except Exception, e:
			logging.debug(e)
			logging.error(pid + ' causes Exception during gameloop')
			self.set_player_result(pid, 'lose')
			self.end(False)
			return

	def on_end(self):
		logging.debug('===GameLoopPhase End===')

	def requestDecision(self):
		logging.debug('Request ' + self.now_turn() + '\'s decision')
		self.request(self.now_turn(),
					 {
			'start': self.cnt
			}
					 )


class ResultPhase(Phase):
	def __init__(self, logic_server, messageType):
		super(ResultPhase, self).__init__(logic_server, messageType)

	def on_start(self):
		logging.debug('===ResultPhase Start===')
		self.cntPlayer = len(self.get_player_list())
		self.sendGameOver()

	def do_action(self, pid, dict_data):
		try:
			args = dict_data
			response = args['response']
			if response != 'OK':
				self.set_player_result(pid, 'error')

			self.cntPlayer -= 1
			if self.cntPlayer == 0:
				logging.debug('All users know that game is over. end the game...')
				self.end(True)
				return

			self.change_turn()
			self.sendGameOver()
			return
		except Exception, e:
			logging.debug(e)
			logging.error(pid + ' causes Exception during result')
			self.set_player_result(pid, 'error')
			self.end(False)
			return

	def on_end(self):
		logging.debug('=======ResultPhase End======')

	def sendGameOver(self):
		logging.debug('Send gameover message to ' + self.now_turn())
		self.request(self.now_turn(), {})


class BaskinServer(TurnGameLogic):
	def __init__(self, game_server):
		super(BaskinServer, self).__init__(game_server)
		sd = self.get_shared_dict()
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
		sd['PHASE_INIT'] = self.append_phase(initPhase)
		sd['PHASE_GAMELOOP'] = self.append_phase(gameloopPhase)
		sd['PHASE_RESULT'] = self.append_phase(resultPhase)
		logging.debug('===BaskinRobbins phase initialization complete===')
		logging.debug('===BaskinRobbins game initialization complete===')

	def on_start(self, player_list):
		super(BaskinServer, self).on_start(player_list)
		logging.debug('===BaskinRobbins game start===')
		self.change_turn(0)
		self.change_phase(0)

	def on_error(self, pid):
		self.set_player_result(pid, 'error')
		self.end(False)
		
