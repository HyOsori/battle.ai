import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic
from gameLogic.baseClass.Phase import Phase
import logging
logging.basicConfig(level=logging.DEBUG)

'''
ShardDict Key

PHASE_INIT -> 'init'->
PHASE_LOOP -> 'loop'->
PHASE_FINISH -> 'finish'->
board
'''

# {"msg":"game_data","msg_type": 정할거,"data":정할거}

class PixelsInitPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsInitPhase, self).__init__(logic_server, message_type)

    def on_start(self):
        super(PixelsInitPhase, self).on_start()
        logging.debug('PixelsInitPhase.on_start')

    def do_action(self, pid, dict_data):
        super(PixelsInitPhase, self).do_action(pid, dict_data)
        logging.debug('PixelsInitPhase.do_action')
        logging.debug('pid : ' + pid)

    def on_end(self):
        super(PixelsInitPhase, self).on_end()
        logging.debug('PixelsInitPhase.on_end')

class PixelsLoopPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsLoopPhase, self).__init__(logic_server, message_type)

    def on_start(self):
        super(PixelsLoopPhase, self).on_start()
        logging.debug('PixelsLoopPhase.on_start')

    def do_action(self, pid, dict_data):
        super(PixelsLoopPhase, self).do_action(pid, dict_data)
        logging.debug('PixelsLoopPhase.do_action')
        logging.debug('pid : ' + pid)

    def on_end(self):
        super(PixelsLoopPhase, self).on_end()
        logging.debug('PixelsLoopPhase.on_end')


class PixelsFinishPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(PixelsFinishPhase, self).__init__(logic_server, message_type)

    def on_start(self):
        super(PixelsFinishPhase, self).on_start()
        logging.debug('PixelsFinishPhase.on_start')

    def do_action(self, pid, dict_data):
        super(PixelsLoopPhase, self).do_action(pid, dict_data)
        logging.debug('PixelsLoopPhase.do_action')
        logging.debug('pid : ' + pid)

    def on_end(self):
        super(PixelsFinishPhase, self).on_end()
        logging.debug('PixelsFinishPhase.on_end')

class PixelsGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(PixelsGameLogic, self).__init__(game_server)

    def on_start(self, player_list):
        logging.debug('PixelsGameLogic.on_start')

        super(PixelsGameLogic, self).on_start(player_list)
        init_phase = PixelsInitPhase(self, 'init')
        loop_phase = PixelsLoopPhase(self, 'loop')
        finish_phase = PixelsFinishPhase(self, 'finish')

        shared_dict = self.get_shared_dict()
        shared_dict['PHASE_INIT'] = self.append_phase(init_phase)
        shared_dict['PHASE_LOOP'] = self.append_phase(loop_phase)
        shared_dict['PHASE_FINISH'] = self.append_phase(finish_phase)

        self.change_turn(0)

        logging.debug('PixelsGameLogic -> InitPhase')
        self.change_phase(0)