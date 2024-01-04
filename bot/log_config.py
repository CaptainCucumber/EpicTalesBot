import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Set httpx logging level to avoid leaking Telegram token in logs.
    # Ideally the token should be reducted by a custom filter.
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Create a rotating file handler
    file_handler = RotatingFileHandler('application.log', maxBytes=1024*1024*5, backupCount=10)
    file_handler.setLevel(logging.INFO)

     # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
