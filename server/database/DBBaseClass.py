class DBBaseClass:
    def __init__(self):
        raise NotImplementedError

    def add_game_log(self, winner, win_score, loser, lose_score):
        raise NotImplementedError

    def del_game_log(self):
        raise NotImplementedError

    def search_game_log(self):
        raise NotImplementedError
