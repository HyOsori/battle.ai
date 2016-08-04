from baskinServer import BaskinServer
import json
#import pdb
#pdb.set_trace()
import logging
logging.basicConfig(level=logging.DEBUG)
import random

class SampleRoom():
	def __init__(self, players):
		self.gamelogic = BaskinServer(self)
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

class SayThreeAI(AI):
	def __init__(self, pid):
		super(SayThreeAI, self).__init__(pid)

	def request(self, messageType, JSON):
		if messageType == 'init':
			return json.dumps({'response' : 'OK'})
		elif messageType == 'gameloop':
			return json.dumps({'num' : 3})
		elif messageType == 'finish':
			return json.dumps({'response' : 'OK'})

class SayOneAI(AI):
	def __init__(self, pid):
		super(SayOneAI, self).__init__(pid)

	def request(self, messageType, JSON):
		if messageType == 'init':
			return json.dumps({'response' : 'OK'})
		elif messageType == 'gameloop':
			return json.dumps({'num' : 1})
		elif messageType == 'finish':
			return json.dumps({'response' : 'OK'})

class MalfunctionedAI(AI):
	def __init__(self, pid):
		super(MalfunctionedAI, self).__init__(pid)

	def request(self, messageType, JSON):
		return json.dumps({})

class SemiMalfunctionedAI(AI):
	def __init__(self, pid):
		super(SemiMalfunctionedAI, self).__init__(pid)

	def request(self, messageType, JSON):
		if messageType == 'init':
			return json.dumps({'response' : 'OK'})
		elif messageType == 'gameloop':
			return json.dumps({'num' : 2})
		elif messageType == 'finish':
			return json.dumps({'response' : 'NOT OK'})

class RandomAI(AI):
	def __init__(self, pid):
		super(RandomAI, self).__init__(pid)

	def request(self, messageType, JSON):
		if messageType == 'init':
			args = json.loads(JSON)
			self.minCnt = args['min']
			self.maxCnt = args['max']
			self.goal = args['finish']
			return json.dumps({'response' : 'OK'})
		elif messageType == 'gameloop':
			return json.dumps({'num' : random.randrange(self.minCnt, self.maxCnt+1)})
		elif messageType == 'finish':
			return json.dumps({'response' : 'OK'})

if __name__ == '__main__':
	x = SampleRoom([SayOneAI('Foo'), SayThreeAI('Bar'), RandomAI('Alice')])
	x.start()