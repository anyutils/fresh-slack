# Configures root logger to log to both stdout and a log file
import logging
from logging.handlers import RotatingFileHandler
import sys

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s [%(levelname)s] -- %(message)s',
    handlers = [
        RotatingFileHandler(
            './fresh-slack.log',
            maxBytes = 500 * 1_000_000
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
