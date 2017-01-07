import logging


def info(msg):
    logging.info("[SERVER]"+str(msg))


def debug(msg):
    logging.debug("[SERVER]"+str(msg))


def error(msg):
    logging.error("[SERVER]"+str(msg))