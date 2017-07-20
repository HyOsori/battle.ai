import logging
import logging.handlers

# build logger instance
logger = logging.getLogger('battle.ai')

# make fomatter
formatter = logging.Formatter('[%(levelname)]')

# make handler
file_handler = logging.FileHandler('./test.log')
stream_handler = logging.StreamHandler()

# put handler on logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# set logger level
logger.setLevel(logging.DEBUG)


