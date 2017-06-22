class DBHelper(object):
    __instance = None

    @classmethod
    def __getinstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__getinstance
        return cls.__instance

    def initialize(self, db):
        self.db = db