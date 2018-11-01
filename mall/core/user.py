# _*_ coding:utf-8 _*_
# Author: nianzong
# 用户信息相关，1.添加用户; 2.用户额度查询; 3.账号锁定操作

import hashlib
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def md5sum(password):
    md5_o = hashlib.md5(bytes(password,encoding="utf-8"))
    return md5_o.hexdigest()

# 提取用户信息to type : dict
user_file = BASE_DIR + '/db/user.txt'
def getuserall():
    d_user = {}
    li_user = []
    with open(user_file,'r') as ufile:
        for line in ufile:
            line = line.strip()
            li_user = line.split(':')
            d_user[li_user[0]] = li_user
    return d_user

d_user = getuserall()
new_user = ""

def islock(username):
    lock_status = d_user[username][3]
    if int(lock_status) == 1:
        return True
    else:
        return False

def dolock(username):
    file_content = ""
    d_user[username][3] = '1'
    for k in d_user:
        file_content += ':'.join(d_user[k]) + '\n'
    with open(user_file,'r+') as ufile:
        ufile.write(file_content)


def adduser():
    while True:
        username = input("input your username:")
        if username.strip() in d_user:
            print("username aleady exist,pls try other name")
        else:
            break
    while True:
        password = input("input password:")
        password_confirm = input("confirm password:")
        if password_confirm != password:
            print("password not match,pls input again")
        else:
            break
    print(username,password)
    new_user=username+':'+md5sum(password)
    with open(user_file,'a+') as ufile:
        ufile.write('\n'+new_user.strip())

TOP_DIR = os.path.dirname(BASE_DIR)
sys.path.append(TOP_DIR)
from atm.core import iccard

def balance(_username):
    """
    获取用户余额
    :param _username: 用户名作为传入参数
    :return:
    """
    with open(user_file,'r') as ufile:
        for line in ufile:
            li_line = line.split(':')
            if _username in li_line:
                if len(li_line) == 4:
                    card_id = li_line[2].strip()
                    user_balance = iccard.readcard(card_id)
                    return user_balance['credit_quota']
                else:
                    return False
