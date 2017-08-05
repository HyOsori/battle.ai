import os
import logging


class ServerLogger(object):
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
        self._logger = logging.getLogger("server")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        import datetime
        now = datetime.datetime.now()
        import time
        timestamp = time.mktime(now.timetuple())

        dirname = './log'
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        file_handler = logging.FileHandler(dirname + "/server")
        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

    def logger(self):
        return self._logger

logger = ServerLogger.instance().logger()
logger.debug("debugging ...")






