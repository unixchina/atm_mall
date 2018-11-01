# _*_ coding:utf-8 _*_
# Author: nianzong

import hashlib
from core import user

# for log
from core import loggers
log_type = 'login'
log_o = loggers.logger(log_type)

# 提取用户信息to type : dict
d_user = user.getuserall()

def md5sum(password):
    md5_o = hashlib.md5(bytes(password,encoding="utf-8"))
    return md5_o.hexdigest()

auth_status = False
user_cur = ''
def auth(func):
    '''
    用户认证函数
    演示密码都是123
    '''
    def inner(*args,**kwargs):
        login_count = 0
        while login_count < 3:
            username = input('username:')
            password = input('password:')
            if username in d_user:
                if md5sum(password) == d_user[username][1].strip():
                    if user.islock(username):
                        print("你的账号处于锁定状态,请联系管理员")
                        exit(0)
                    else:
                        print('Login success,Welcome %s' %username)
                        log_o.info("Login success - account:%s" %(username))
                        auth_status = True
                        break
                else:
                    login_count += 1
                    print('password error,pls try again')
                    log_o.error("Login failed - account:%s" %(username))
            else:
                print('This account is not exist.')
        else:
            user.dolock(username)
            print('你的账号已被锁定,请联系管理员解锁! ')
            log_o.error("Account locked! - account:%s" %(username))
            exit(0)
        if auth_status == True:
            global user_cur
            user_cur = username
            return func(*args, **kwargs)
    return inner

