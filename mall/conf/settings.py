# _*_ coding:utf-8 _*_
# Author: nianzong
import logging
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = "%s/db" % BASE_DIR

def getdbpath(*args):
    if len(args):       #"lenth is not 0"
        if os.path.exists("%s/%s" % (DB_PATH,args[0])):
            return "%s/%s" % (DB_PATH,args[0])
        else:
            return False
    else:
        print("lenth is 0")
        return DB_PATH

LOG_BASE_LEVEL = logging.DEBUG
LOG_HANDLER_LEVEL = logging.INFO

LOG_TYPES = {
    'login': BASE_DIR + '/logs/login.log',
    'buy': BASE_DIR + '/logs/buy_history.log'
}
