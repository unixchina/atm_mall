# _*_ coding:utf-8 _*_
# Author: nianzong
# 1. 登录or注册新用户;
# 2. 显示商品列表-添加到购物车-结账[调信用卡接口,需要进行认证]

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import cart

cart.carts()
