# atm_mall
# 模拟atm取款机业务,mall购物商城
'''
运行环境:Python3
在Centos6.8/win10+Pycharm  Python3.6.5下运行过.
'''
演示:
商城登录用户密码为123,默认只创建了两个账号:alex/tom,密码相同.
ATM定义了两个账号[卡号]:1234/2234,密码都是sdf
'''
ATM_MALL
├── atm                     # ATM程序目录
│   ├── account
│   │   ├── 1234.json           # 账号1对应的信息文件,包含卡号/余额/还款额/非明文密码等
│   │   └── 2234.json           # 账号1对应的信息文件,包含卡号/余额/还款额/非明文密码等
│   ├── bin
│   │   ├── atm_entrance.py     # ATM程序的主入口
│   │   └── __init__.py
│   ├── conf
│   │   └── setting.py          # 配置文件,定义了日志级别等信息
│   ├── core
│   │   ├── get_card_id.py      # 获取卡号信息[现实中读取芯片信息,本项目中定义了一个默认的插入卡号]
│   │   ├── iccard.py           # 银行卡的存取相关操作,包括了扣款/还款接口
│   │   ├── __init__.py
│   │   ├── logger.py           # 定义日志操作模块
│   │   ├── login_auth.py       # 用户登录认证
│   │   ├── transfer.py         # 转账模块
│   │   └── withdraw.py         # 取现模块
│   ├── __init__.py
│   └── logs                    # 登录与交易日志
│       ├── login.log
│       └── trade.log
├── __init__.py
└── mall                    # 购物商城目录
    ├── bin
    │   ├── __init__.py
    │   └── mall.py             # 购物商城入口
    ├── conf
    │   ├── __init__.py
    │   └── settings.py         # 配置
    ├── core
    │   ├── cart.py             # 购物商城核心程序
    │   ├── goods.py            # 商品相关
    │   ├── __init__.py
    │   ├── loggers.py          # 日志模块
    │   ├── login.py            # 用户登录
    │   └── user.py             # 用户相关,包括用户信息,添加用户,锁操作,余额查询接口
    ├── db
    │   ├── bought_list.txt     # 购买商品数据
    │   ├── goods.txt           # 商品数据
    │   └── user.txt            # 商城用户数据
    ├── __init__.py
    └── logs
        ├── buy_history.log     # 用户购买商品的日志
        ├── login.log           # 登录日志
