# _*_ coding:utf-8 _*_
# Author: nianzong

import time
import hashlib
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP_DIR = os.path.dirname(BASE_DIR)
sys.path.append(TOP_DIR)
from atm.core import logger

def md5sum(password):
    md5_o = hashlib.md5(bytes(password,encoding="utf-8"))
    return md5_o.hexdigest()

auth_status = False

def auth(card_id):
    log_type = 'login'
    log_o = logger.logger(log_type)
    def outter(func):
        def inner(*args,**kwargs):
            from core import iccard
            data_card = iccard.readcard(card_id)
            count = 0
            while count < 3:
                user_input = input("Pls input password:")
                if md5sum(user_input) == data_card['password']:
                    if data_card['lock_status'] == 1:
                        print("您的账号处于锁定状态,请到柜台进行处理.")
                        return False
                    else:
                        if time.strftime('%Y-%m-%d') > data_card['expire_date']:
                            print("Your account has expired.Pls contact counter staff.")
                        else:
                            print("Login sucess!")
                            log_o.info("Login sucess - account:%d" %(card_id))
                            auth_status = True
                            break
                else:
                    print("密码错误,请重新输入.")
                    count += 1
                    continue
            else:
                print("密码输入错误已达3次,您的账号已被锁定,请到柜台进行处理.")
                data_card['lock_status'] = 1
                iccard.writecard(data_card,card_id)
                log_o.error("Too many attempts account:%d - account was locked " % (card_id))
                return 'account lock'
            if auth_status == True:
                return func(*args,**kwargs)
        return inner
    return outter

