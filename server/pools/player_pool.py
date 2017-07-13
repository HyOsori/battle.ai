class PlayerPool(object):
    def __init__(self):
        # key: player name
        # value: player object
        self.__players = dict()

    def __iter__(self):
        return self.__players.values().__iter__()

    def add_player(self, player):
        self.__players[player._id] = player

    def remove_player(self, player):
        if player._id in self.__players.keys():
            self.__players.pop(player._id)

    def get_player(self, _id):
        if _id in self.__players.keys():
            return self.__players.get(_id)
        else:
            return None

