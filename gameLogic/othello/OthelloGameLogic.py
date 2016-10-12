#-*-coding:utf-8-*-
import sys
sys.path.insert(0,'../')
from gameLogic.baseClass.TurnGameLogic import TurnGameLogic
from gameLogic.baseClass.Phase import Phase
#import json
import logging
logging.basicConfig(level=logging.DEBUG)

'''
ShardDict Key

PHASE_ONTURN -> 'on_turn'->
PHASE_END    -> 'finish'->
board

'''

class OthelloOnTurnPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(OthelloOnTurnPhase, self).__init__(logic_server, message_type)

    def on_start(self):
        super(OthelloOnTurnPhase,self).on_start()
        logging.debug('##OthelloOnTurnPhase Start')
        self.player_list = self.get_player_list()
        shard_dict = self.get_shared_dict()

        self.black = self.player_list[0]
        self.white = self.player_list[1]
        self.none = 'NONE'
        self.board = shard_dict['board']
        self.next_phase = shard_dict['PHASE_END']

        self.change_turn(0)
        self.request_and_send_board()

    def do_action(self, pid, dict_data): # need args -> [turn , x , y]
        super(OthelloOnTurnPhase,self).do_action(pid, dict_data)
        logging.debug('OthelloOnTurnPhase doAction from ' + pid + ' Processing...')
        if pid != self.now_turn():
            result = dict(zip(self.player_list, ['win'] * len(self.player_list)))
            result[pid] = 'lose'
            logging.error(pid + ' is not equal to current turn player;' + self.now_turn())
            self.end(False, result)
            return

        try:
            action_info = dict_data
            x = int(action_info['x'])
            y = int(action_info['y'])

            if self.is_valid_move(pid, x, y) == False:
                result = dict(zip(self.player_list, ['win'] * len(self.player_list)))
                result[pid] = 'lose'
                logging.error(pid+' invalid Move')
                self.end(False, result)
                return

            if pid == self.white:
                oppsite = self.black
            else:
                oppsite = self.white

            validMoves = self.get_valid_moves(pid)

            if validMoves != []:
                self.make_move(pid, x, y) # change board
                self.notify_board(pid, x, y) # notify change board


            if self.is_game_end():
                self.change_phase(self.next_phase)
                return

            if self.get_valid_moves(oppsite) != []:
                self.change_turn()


            self.request_and_send_board()

        except Exception, e:
            logging.debug(e)
            logging.error(pid+' causes Exception during OthelloOnTurnPhase')
            result = dict(zip(self.player_list, ['win'] * len(self.player_list)))
            result[pid] = 'lose'
            self.end(False, result)

    def is_valid_move(self, tile, xstart, ystart):
        if self.board[xstart][ystart] != self.none or not self.is_on_board(xstart, ystart):
            return False

        self.board[xstart][ystart] = tile  # temporarily set the tile on the board.

        if tile == self.black:
            other_tile = self.white
        else:
            other_tile = self.black

        tiles_to_flip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            if self.is_on_board(x, y) and self.board[x][y] == other_tile:
                x += xdirection
                y += ydirection
                if not self.is_on_board(x, y):
                    continue
                while self.board[x][y] == other_tile:
                    x += xdirection
                    y += ydirection
                    if not self.is_on_board(x, y):
                        break
                if not self.is_on_board(x, y):
                    continue
                if self.board[x][y] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tiles_to_flip.append([x, y])

        self.board[xstart][ystart] = self.none
        if len(tiles_to_flip) == 0:
            return False
        return tiles_to_flip

    def is_on_board(self, x, y):
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def get_valid_moves(self, tile):
        valid_moves = []

        for x in range(8):
            for y in range(8):
                if self.is_valid_move(tile, x, y) != False:
                    valid_moves.append([x, y])
        return valid_moves

    def make_move(self, tile, xstart, ystart):
        tiles_to_flip = self.is_valid_move(tile, xstart, ystart)

        if tiles_to_flip == False:
            return False

        self.board[xstart][ystart] = tile
        for x, y in tiles_to_flip:
            self.board[x][y] = tile
        return True

    def on_end(self):
        super(OthelloOnTurnPhase,self).on_end()
        logging.debug('##OthelloOnTurnPhase End')

    def is_game_end(self):
        b_count = 0
        w_count = 0

        for x in range(8):
            for y in range(8):
                if self.board[x][y] == self.black:
                    b_count = b_count+1
                elif self.board[x][y] == self.white:
                    w_count = w_count+1

        if (b_count == 0) or (w_count == 0) or (b_count+w_count == 64):
            return True
        return False

    def change_board_to_integer(self):
        int_board = [[0 for col in range(8)] for row in range(8)]
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == self.none:
                    int_board[x][y] = 0
                elif self.board[x][y] == self.black:
                    int_board[x][y] = 1
                elif self.board[x][y] == self.white:
                    int_board[x][y] = 2

        return int_board

    def notify_board(self, pid, x, y):
        int_board = self.change_board_to_integer()
        notifyDict = {
            'board' : int_board,
            'x' : x,
            'y' : y,
            'black' : self.black,
            'white' : self.white,
            'now_turn' : pid
        }

        self.notify(notifyDict)

    def request_and_send_board(self):
        logging.debug('Request ' + self.now_turn() + '\'s decision')
        info_dict = {
            'board': self.board,
            'black': self.black,
            'white': self.white,
            'none': self.none
        }
        self.request(self.now_turn(), info_dict)

class OthelloEndPhase(Phase):
    def __init__(self, logic_server, message_type):
        super(OthelloEndPhase,self).__init__(logic_server, message_type)

    def on_start(self):
        super(OthelloEndPhase, self).on_start()
        logging.debug('OthelloEndPhase Start')
        self.player_list = self.get_player_list()
        shard_dict = self.get_shared_dict()
        self.black = self.player_list[0]
        self.white = self.player_list[1]

        self.cnt_player = 2
        self.board = shard_dict['board']

        self.send_game_over()

    def get_score_of_board(self):
        black_score = 0
        white_score = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == self.black:
                    black_score += 1
                if self.board[x][y] == self.white:
                    white_score += 1

        result_dict = {
            'black_score' : black_score,
            'white_score' : white_score
        }

        if black_score > white_score:
            result_dict['win'] = self.black
            result_dict['lose'] = self.white
        elif white_score > black_score:
            result_dict['win'] = self.white
            result_dict['lose'] = self.black
        else:
            result_dict['draw'] = True

        return result_dict

    def do_action(self, pid, dict_data):
        # args is not using
        super(OthelloEndPhase, self).do_action(pid, dict_data)
        try:
#            args = dictData
#            response = args['response']
#            if response != 'OK':
#                self.setPlayerResult(pid,'error')

            self.cnt_player -= 1

            if self.cnt_player == 0:
                result_dict = self.get_score_of_board()
                self.notify_winner(result_dict)
                logging.error(pid + ' **************************')
                send_dict = {result_dict['win']:'win',
                                    result_dict['lose']:'lose',
                                    'black_score':result_dict['black_score'],
                                    'white_score':result_dict['white_score']}
                self.end(True, send_dict)
                return

            self.change_turn()
            self.send_game_over()

        except Exception, e:
            logging.debug(e)
            logging.error(pid + ' causes Exception during result')
            result = dict(zip(self.player_list, ['win'] * len(self.player_list)))
            result[pid] = 'lose'
            self.end(False, result)

    def on_end(self):
        super(OthelloEndPhase, self).on_end()
        logging.debug('===ResultPhase End===')

    def notify_winner(self, winner_dict):
        notify_dict = winner_dict

        self.notify(notify_dict)

    def send_game_over(self):
        logging.debug('Send gameover message to ' + self.now_turn())
        self.request(self.now_turn(), {})

#######################################
#######################################

##messageType -> onTurn = {x,y}
##            -> finish = {response}
##
class OthelloGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(OthelloGameLogic, self).__init__(game_server)
        self.none = "NONE"
        self.board = [[self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none]]


        logging.debug('Othello Logic Init')
        logging.debug('LogicServer init finish')

    def on_start(self, player_list):
        super(OthelloGameLogic, self).on_start(player_list)
        self.black = player_list[0]  # first player's name
        self.white = player_list[1]  # second player's name
        self.board = [[self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.white, self.black, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.black, self.white, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none],
                      [self.none, self.none, self.none, self.none, self.none, self.none, self.none, self.none]]

        shard_dict = self.get_shared_dict()
        shard_dict['board'] = self.board
        logging.debug('Othello Phase Init')

        on_turn_phase = OthelloOnTurnPhase(self, 'on_turn')
        end_phase = OthelloEndPhase(self, 'finish')
        shard_dict['PHASE_ONTURN'] = self.append_phase(on_turn_phase)
        shard_dict['PHASE_END'] = self.append_phase(end_phase)

        logging.debug('Phase init finish')

        logging.debug('Othello Game Start')
        self.change_turn(0)
        self.change_phase(0)

    def on_error(self, pid):
        super(OthelloGameLogic, self).on_error(pid)
