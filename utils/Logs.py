import logging
import sys

def get_logger(logger_name, level=logging.INFO):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    file_handler = logging.FileHandler('all.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel(logging.ERROR)
    logger.addHandler(consoleHandler)

    return logger
