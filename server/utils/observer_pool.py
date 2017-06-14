class ObserverPool(object):
    def __init__(self):
        self.__observers = set()

    def add_observer(self, observer):
        self.__observers.add(observer)

    def remove_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)
