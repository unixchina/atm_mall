# _*_ coding:utf-8 _*_
# Author: nianzong
from conf import setting
from core import logger

def withdraw(data,R_O_INT=0.05):
    log_type = 'trade'
    trade_type = setting.TRADE_TYPE[1]
    log_o = logger.logger(log_type)

    withdraw_money = input("输入提现额度: ")
    if int(withdraw_money) < data['credit_quota'] / 2:
        data['credit_quota'] = data['credit_quota'] - int(withdraw_money)
        interest = int(withdraw_money) * R_O_INT
        data['repayment'] = data['repayment'] + int(withdraw_money) + interest
        log_o.info("trade_type:%s - card_id:%d - amount:%.2f interest:%.2f" %
                           (trade_type,data['card_id'],int(withdraw_money),interest))
    else:
        print("\033[1;33;40m","提现超额", "\033[0m")
        log_o.error("trade_type:%s - card_id:%d - amount:%.2f - [Withdrawal excess]" %
                   (trade_type,data['card_id'], int(withdraw_money)))
        return False
    return data