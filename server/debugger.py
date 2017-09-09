import logging

FLAG = "[SERVER]"
BLANK = " "

logging.basicConfig(level=logging.DEBUG)

def info(msg):
    logging.info(FLAG+BLANK+str(msg))


def debug(msg):
    logging.debug(FLAG+BLANK+str(msg))


def error(msg):
    logging.error(FLAG+BLANK+str(msg))
