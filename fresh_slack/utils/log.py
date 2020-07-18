'''
Configures root logger to log to both stdout and a log file
'''
import logging
import sys


logFormatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] -- %(message)s',
    datefmt = '%Y-%m-%dT%H:%M:%S%z'
)
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler('./fresh-slack.log')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


def debug(msg: str) -> None:
    logging.debug(msg)

def info(msg: str) -> None:
    logging.info(msg)

def warn(msg: str) -> None:
    logging.warn(msg)

def error(msg: str) -> None:
    logging.error(msg)
