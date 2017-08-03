import logging
import os


class Logger(object):
    __instance = None

    @classmethod
    def __getinstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__getinstance()
        return cls.__instance

    def __init__(self):
        pass
