import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def setup_logging(use_console):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        'logs/transactions_manager.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    if use_console:
        logger.addHandler(console_handler)

    logger.addHandler(file_handler)
    return logger