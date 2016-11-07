WINNER = "winner"
WIN_SCORE = "win_score"
LOSER = "loser"
LOSER_SCORE = "loser_score"
DRAW = "draw"


class GameLogManager:
    def __init__(self, db_conn=None):
        self.db_conn = db_conn
        self.cur = 0
        self.size = 0
        self.max_size = 200
        self.log = [0 for x in range(self.max_size)]

    def make_result(self, winner, win_score, loser, loser_score):
        return {WINNER: winner, WIN_SCORE: win_score, LOSER: loser, LOSER_SCORE: loser_score, DRAW: True}

    def add_game_log(self, winner, win_score, loser, loser_score):
        result = self.make_result(winner, win_score, loser, loser_score)
        self.log[self.cur] = result
        self.cur += 1
        if self.cur == 200:
            self.cur = 0

        if not self.size == 200:
            self.size += 1

    def print_all(self):
        for i  in len(self.size):
            print self.log[(i+self.cur)%self.max_size]