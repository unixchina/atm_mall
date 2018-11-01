# _*_ coding:utf-8 _*_
# Author: nianzong
import os,sys
BASE_DIR = os.path.dirname(sys.path[0])
sys.path.append(BASE_DIR)

import json
from conf import settings

# 提取商品信息
goods_file = settings.getdbpath('goods.txt')

def getgoods():
    gfo = open(goods_file,'r',encoding='UTF-8')
    dict_goods = json.load(gfo)
    gfo.close()
    return dict_goods
