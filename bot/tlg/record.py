import logging
import os
from logging.handlers import RotatingFileHandler

from config import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False


def setup_logging():
    log_file = config.get_log_path() + "/records.log"
    log_directory = os.path.dirname(log_file)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=1024 * 1024 * 10, backupCount=50
    )
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def record_message(message: dict):
    logger.info(message)


if not logger.handlers:
    setup_logging()
