# _*_ coding:utf-8 _*_
# Author: nianzong
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import user
from core import login
from core import goods

# for log
from core import loggers
log_type = 'buy'
log_o = loggers.logger(log_type)
'''
显示商品清单后,可以添加商品到购物车.用户下单时扣款需对绑定卡号进行认证.
购买记录格式: 时间戳-日志类型-日志级别-账号-商品名称-消费金额
'''
# Login:
@login.auth
def carts():
    user_cur = login.user_cur
    username = user_cur
    # 用户信息取出存储到字典中
    dict_user = user.getuserall()

    # 提取商品信息
    dict_goods = goods.getgoods()

    # 获取用户余额
    funds_content = ""
    dict_funds = {}
    dict_funds[user_cur] = balance_cur = user.balance(user_cur)

    # 用户已买到商品
    bought_file = BASE_DIR + '/db/bought_list.txt'
    bought_content = ""
    dict_bought = {}

    # 读取当前购买记录存储到字典dict_bought
    with open(bought_file,'r',encoding='utf-8') as boughtfile:
        for bline in boughtfile:
            bline = bline.strip()
            if not len(bline):
                continue
            bline_list = bline.split(":")
            dict_bought[bline_list[0]] = eval(bline_list[1])

    # 购物车列表初始化
    cart_list = []
    # 本次购买记录
    buy_list_today = []
    buy_one_round = {}
    goods_count = 0

    TOP_DIR = os.path.dirname(BASE_DIR)
    sys.path.append(TOP_DIR)
    from atm.core import iccard
    card_id = int(dict_user[username][2])
    card_data = iccard.readcard(card_id)

    # 登陆后进入商品菜单，选择商品添加到购物车，结账等流程
    while True:
        for n,d in dict_goods.items():
            print("{:^4}\t{:<8}\tprice:{:<6}" .format(n,d['name'],d['price']))
        print("[商品编号 - 添加对应商品到购物车]","[cart - 进入购物车]","[bh - 查询购买记录]","[bal - 余额查询]","[q - 退出程序]")
        choose_goods = input('\033[5;34;47mPls choose a goods you want to buy into shopping cart:\033[0m')

        if choose_goods == 'cart':
            while True:
                print('当前购物车商品:','\033[1;33;40m',cart_list,'\033[0m')
                print("[q -- 退出程序]","[order -- 确认订单并付款]","[gl -- 回到商品列表继续选择商品]")
                confirm_order = input('请选择对应的功能键:')
                if confirm_order == 'order':
                    cart_price_sum = 0
                    for n in buy_one_round:
                        cart_price_sum += buy_one_round[n]['price'] * buy_one_round[n]['count']

                    if cart_price_sum > balance_cur:
                        del_cart_goods = input('您的金额不足,请从购物车中删除部分商品:')
                        if del_cart_goods in cart_list:
                            cart_list.remove(del_cart_goods)
                            count_now = buy_one_round[del_cart_goods]['count']
                            buy_one_round[del_cart_goods]['count'] = count_now - 1
                        else:
                            print('输入错误')

                    # 金额充足进入扣款流程
                    else:
                        # 资金结余
                        dict_funds[username] = balance_cur - cart_price_sum
                        retval = iccard.deduction(card_id,cart_price_sum)
                        if retval == False:
                            print("卡号密码输入错误")
                            break
                        # 新增已购买到的商品列表到dict_bought
                        if username in dict_bought:
                            dict_bought[username].extend(cart_list)
                        else:
                            dict_bought[username] = cart_list

                        for k in dict_bought:
                            bought_content += k + ":" + str(dict_bought[k]) + "\n"
                        with open(bought_file,'r+',encoding='utf-8') as boughtfile:
                            boughtfile.write(bought_content)
                            bought_content = ""
                        print("您本轮所购商品为:""\033[1;33;40m", cart_list, "\033[0m",
                              "消费金额为:""\033[1;33;40m", cart_price_sum, "\033[0m")
                        log_o.info("account:%s - goods:%s - pay amount:%d" %(username,cart_list,cart_price_sum))

                        # 结账完毕后清空购物车,退出购物车可继续购物
                        buy_list_today.extend(cart_list)
                        cart_list.clear()
                        goods_count = 0
                        buy_one_round = {}
                        balance_cur = dict_funds[username]
                        break
                elif confirm_order == 'q':
                    print("您本次所购商品为:""\033[1;33;40m",buy_list_today,"\033[0m",
                          "您的余额为:""\033[1;33;40m",dict_funds[username],"\033[0m")
                    print('欢迎下次再来,Bye!')
                    return
                elif confirm_order == 'gl':
                    break
                else:
                    print('\033[1;31;40m', '您的输入有误,请输入正确选项!', '\033[0m','\n')
        elif choose_goods.isdigit():
            if choose_goods in dict_goods:
                print('你选择的商品是:','\033[1;33;40m',choose_goods,'--',dict_goods[choose_goods],'\033[0m')
                goods_id = choose_goods
                print('goods_id:',goods_id)
                if dict_goods[goods_id]['name'] in cart_list:
                    buy_one_round[dict_goods[goods_id]['name']]['count'] += 1
                else:
                    buy_one_round[dict_goods[goods_id]['name']] = {'itemid':goods_id,'price':dict_goods[goods_id]['price'],'count':0}
                    buy_one_round[dict_goods[goods_id]['name']]['count'] = 1
                cart_list.append(dict_goods[goods_id]['name'])
                print('你可以继续添加商品,或者进入购物车结账')
            else:
                print("请输入正确的商品编号")
        elif choose_goods == 'q':
            if not len(buy_list_today):
                dict_funds[username] = balance_cur
                # 用户登陆后没有购买商品就退出
            print("您本次所购商品为:""\033[1;33;40m", buy_list_today, "\033[0m",
                  "您的余额为:""\033[1;33;40m", dict_funds[username], "\033[0m")
            print('欢迎下次再来,Bye!')
            break
        elif choose_goods == 'bh':
            with open(bought_file,'r',encoding='utf-8') as boughtfile:
                for bline in boughtfile:
                    bline = bline.strip()
                    bline_list = bline.split(":")
                    dict_bought[bline_list[0]] = eval(bline_list[1])
            if username in dict_bought:
                bought_hist = dict_bought[username]
            else:
                bought_hist = ""
            print('您购买的所有商品记录:''\033[1;33;40m', bought_hist, '\033[0m')
            continue
        elif choose_goods == 'bal':
            print("您银行卡余额为:",dict_funds[user_cur])
        else:
            print('\033[1;31;40m','输入错误,请输入正确的商品编号或选项!','\033[0m')
