class LobbyPool(object):
    def __init__(self):
        self.__lobby_user = set()

    def add_lobby_user(self, lobby_user):
        self.__lobby_user.add(lobby_user)

    def remove_lobby_user(self, lobby_user):
        if lobby_user in self.__lobby_user:
            self.__lobby_user.remove(lobby_user)
