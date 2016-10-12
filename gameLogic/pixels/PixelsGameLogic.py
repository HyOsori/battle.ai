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

class PixelsInitPhase(Phase):
    def on_start(self):
        pass

    def do_action(self, pid, dict_data):
        pass

    def on_end(self):
        pass

class PixelsLoopPhase(Phase):
    def on_start(self):
        pass

    def do_action(self, pid, dict_data):
        pass

    def on_end(self):
        pass


class PixelsFinishPhase(Phase):
    def on_start(self):
        pass

    def do_action(self, pid, dict_data):
        pass

    def on_end(self):
        pass

class PixelsGameLogic(TurnGameLogic):
    def on_start(self, player_list):
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