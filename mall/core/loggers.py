# _*_ coding:utf-8 _*_
# Author: nianzong
import os
import sys
import logging
from logging import handlers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
def logger(log_type):
    logger_obj = logging.getLogger(log_type)
    if not logger_obj.handlers:
        logger_obj.setLevel(settings.LOG_BASE_LEVEL)

        # file log formatter:
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logfile = settings.LOG_TYPES[log_type]

        file_handler = handlers.TimedRotatingFileHandler(logfile,encoding='utf-8',when="midnight", interval=1, backupCount=60)
        file_handler.setLevel(settings.LOG_HANDLER_LEVEL)

        logger_obj.addHandler(file_handler)
        file_handler.setFormatter(file_formatter)

    return logger_obj


