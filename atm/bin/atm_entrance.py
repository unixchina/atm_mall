# _*_ coding:utf-8 _*_
# Author: nianzong

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import get_card_id
from core import login_auth
from core import withdraw
from core import iccard
from core import transfer


menu = """
    ------- Python Bank ---------
    1.  账户信息
    2.  转账
    3.  提现
    4.  还款
    5.  退出
"""

default_id = get_card_id.getid()
id = default_id
# id = 2234       # 测试用,注释掉则默认卡号为1234

# login:
@login_auth.auth(id)
def run():
    '''
    登录后主菜单
    为便于演示,默认当前插入卡号为1234,转账卡号为2234.登录密码为[sdf]
    :return:
    '''
    card_id = id

    while True:
        data_card = iccard.readcard(card_id)
        print(menu)
        input_choice = input("选择菜单中的选项:")

        while input_choice != '5':

            if input_choice == '1':
                print("\n账号: %d\t信用额度: %.2f\t还款额: %.2f" %
                      (data_card['card_id'],data_card['credit_quota'],data_card['repayment']))
                break
            elif input_choice == '2':
                trans_id = int(input("请输入对方卡号: ").strip())
                transfer_amount = int(input("请输入转账金额[整额]: ").strip())
                data_card = transfer.trans_money(card_id,trans_id,transfer_amount)

                break
            elif input_choice == '3':
                data_card = withdraw.withdraw(data_card)
                if data_card == False:
                    break
                else:
                    iccard.writecard(data_card,card_id)
                    break
            elif input_choice == '4':
                amount = float(input("请输入还款金额:").strip())
                iccard.repayment(card_id,amount)
                break
            else:
                print("输入错误!")
                break
        else:
            print("\nBye!")
            exit(0)


if __name__ == '__main__':
    run()
