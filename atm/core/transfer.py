# _*_ coding:utf-8 _*_
# Author: nianzong
"""
信用卡转账基本流程：
    1. 插入银行卡，输入密码，进入界面，选择'转账业务'
    2. 输入对方账号
    3. 输入转账金额 (由于信用卡特性,转账金额上限不超过剩余额度的一半)
    4. 确认对方账号与金额 (判断账号是否存在,金额是否合理)
"""
import os,sys
from core import iccard
from conf import setting
from core import logger
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def trans_money(my_id,trans_id,amount):
    trans_msg_confirm = """
    确认转账信息:
        对方卡号: %s
        转账金额: %s
    """ % (trans_id, amount)
    data_card = iccard.readcard(my_id)
    data_card2 = iccard.readcard(trans_id)
    trans_file = BASE_DIR + "/account/%s"%trans_id + ".json"
    log_type = 'trade'
    trade_type = setting.TRADE_TYPE[0]      # transfer
    log_o = logger.logger(log_type)
    print(trans_msg_confirm)
    if os.path.exists(trans_file):
        if int(trans_id) == data_card2['card_id']:
            if int(amount) <= data_card['credit_quota'] / 2:
                data_card['credit_quota'] = data_card['credit_quota'] - int(amount)
                data_card['repayment'] = data_card['repayment'] + int(amount)
                data_card2['credit_quota'] = data_card2['credit_quota'] + int(amount)
                data_card2['repayment'] = data_card2['repayment'] - int(amount)

                iccard.writecard(data_card,my_id)
                iccard.writecard(data_card2,trans_id)
                log_o.info("trade_type:%s - card_id:%d - to_card:%d - amount:%.2f" %
                           (trade_type,my_id,trans_id,amount))

            else:
                log_o.error("trade_type:%s - card_id:%d - to_card:%d - amount:%.2f - [Transfer amount exceeded limit]" %
                           (trade_type,my_id,trans_id,amount))
                print("转账失败,转账金额超限!")
        else:
            print("转账失败,账号不存在!")
            print(trans_id)
            return False
    else:
        print("系统错误,数据文件不存在")
        print(trans_file)

    return data_card
