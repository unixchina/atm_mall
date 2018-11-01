# _*_ coding:utf-8 _*_
# Author: nianzong

import logging

LOG_BASE_LEVEL = logging.DEBUG
LOG_HANDLER_LEVEL = logging.INFO

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_TYPES = {
    'trade': BASE_DIR + '/logs/trade.log',
    'login': BASE_DIR + '/logs/login.log',
}

TRADE_TYPE = [
    'transfer',
    'withdraw',
    'deduction',
    'repayment'
]
