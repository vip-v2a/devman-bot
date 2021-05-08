import logging
from logging.handlers import RotatingFileHandler

STRFMT = '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
DATEFFMT = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger('bot logger')
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler("bot_log.log", maxBytes=1024, backupCount=2)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt=STRFMT, datefmt=DATEFFMT)
handler.setFormatter(formatter)
logger.addHandler(handler)