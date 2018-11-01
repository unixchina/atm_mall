# _*_ coding:utf-8 _*_
# Author: nianzong
import json
import os,sys

WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(WORK_DIR)
TOP_DIR = os.path.dirname(WORK_DIR)
sys.path.append(TOP_DIR)
from atm.core import logger

def readcard(card_id):
    json_file = str(card_id) + ".json"
    iccard_file = WORK_DIR + "/account/" + json_file
    ufo = open(iccard_file, 'r+', encoding='utf-8')
    d_card = json.load(ufo)
    ufo.close()
    return d_card

def writecard(data,card_id):
    json_file = str(card_id) + ".json"
    iccard_file = WORK_DIR + "/account/" + json_file
    ufo = open(iccard_file, 'r+', encoding='utf-8')
    if data['credit_quota'] >= 0:
        ufo.seek(0)
        ufo.truncate()
        json.dump(data,ufo)
        ufo.close()
        return True
    else:
        ufo.close()
        return False

def deduction(card_id,amount):
    '''
    结账扣款
    :param card_id: 卡号
    :param amount: 金额
    :return:
    '''

    TOP_DIR = os.path.dirname(WORK_DIR)
    sys.path.append(TOP_DIR)
    from atm.core.login_auth import md5sum
    from atm.conf import setting
    log_type = 'trade'
    trade_type = setting.TRADE_TYPE[2]   #repayment
    log_o = logger.logger(log_type)
    data = readcard(card_id)
    userpwd = input("Pls input card password:").strip()
    if md5sum(userpwd) == data['password']:
        data['credit_quota'] = data['credit_quota'] - amount
        data['repayment'] = data['repayment'] + amount
        retval = writecard(data,card_id)
        if retval == True:
            log_o.info("trade_type:%s - card_id:%d - amount:%.2f" % (trade_type, card_id, amount))
        else:
            log_o.error("trade_type:%s - card_id:%d - amount:%.2f - [Insufficient Balance]"
                        % (trade_type, card_id, amount))
    else:
        return False

def repayment(card_id,amount):
    '''
    ATM存入还款
    :param card_id: 卡号
    :param amount: 还款金额
    :return:
    '''
    from conf import setting
    log_type = 'trade'
    trade_type = setting.TRADE_TYPE[3]   #repayment
    log_o = logger.logger(log_type)

    data = readcard(card_id)
    data['credit_quota'] = data['credit_quota'] + amount
    data['repayment'] = data['repayment'] - amount
    writecard(data,card_id)
    log_o.info("trade_type:%s - account:%d - amount:%.2f" %(trade_type,card_id,amount))
    print("您本次还款金额为:",amount)