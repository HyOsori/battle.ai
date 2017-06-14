class PlayerPool(object):
    def __init__(self):
        # key: player name
        # value: player object
        self.__players = dict()

    def add_player(self, player):
        self.__players[player.name] = player

    def remove_player(self, player):
        if player.name in self.__players.keys():
            self.__players.pop(player.name)


