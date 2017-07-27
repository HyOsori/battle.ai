class SingleTonType(type):
    def instance(self, *args, **kwargs):
        try:
            return self.__instance
        except AttributeError:
            self.__instance = super(SingleTonType, self).__call__(*args, **kwargs)
            return self.__instance
