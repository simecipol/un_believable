import logging
import os

def init():
    logger = logging.getLogger("un_believable")
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level, logging.INFO)
    logger.setLevel(log_level) 
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

