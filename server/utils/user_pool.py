from server.utils.player_pool import PlayerPool
from server.utils.lobby_pool import LobbyPool
from server.utils.observer_pool import ObserverPool

'''
Singleton instance to control all user in this application
'''


class UserPool(object):

    __instance = None

    @classmethod
    def __getinstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__getinstance
        return cls.__instance

    def __init__(self):
        self.player_pool = PlayerPool()
        self.lobby_pool = LobbyPool()
        self.observer_pool = ObserverPool()

    def get_player_pool(self):
        return self.player_pool

    def get_lobby_pool(self):
        return self.lobby_pool

    def get_observer_pool(self):
        return self.observer_pool


a = UserPool.instance()
b = UserPool.instance()

print(a)
print(b)

a.get_player_pool().append("a")
print(b.get_player_pool())

