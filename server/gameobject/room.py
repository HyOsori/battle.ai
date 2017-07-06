
class Room:
    def __init__(self, players=[], observer=None):
        self.player_list = players
        self.observer_list = []
        self.game = None

        if observer:
            self.add_observer(observer)

    def add_observer(self, observer):
        self.observer_list.append(observer)

    def del_observer(self, observer):
        self.observer_list.pop(observer)




