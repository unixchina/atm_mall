# _*_ coding:utf-8 _*_
# Author: nianzong
import os
import sys
import logging
from logging import handlers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP_DIR = os.path.dirname(BASE_DIR)
sys.path.append(TOP_DIR)


def logger(log_type):
    from atm.conf import setting
    logger_obj = logging.getLogger(log_type)
    if not logger_obj.handlers:                 # 避免重复写日志
        logger_obj.setLevel(setting.LOG_BASE_LEVEL)

        # file log formatter:
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logfile = setting.LOG_TYPES[log_type]

        file_handler = handlers.TimedRotatingFileHandler(logfile,encoding='utf-8',when="midnight", interval=1, backupCount=60)
        file_handler.setLevel(setting.LOG_HANDLER_LEVEL)

        logger_obj.addHandler(file_handler)
        file_handler.setFormatter(file_formatter)

    return logger_obj

