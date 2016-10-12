import logging


def info(msg):
    logging.info("[SERVER]"+msg)


def debug(msg):
    logging.debug("[SERVER]"+msg)


def error(msg):
    logging.error("[SERVER]"+msg)