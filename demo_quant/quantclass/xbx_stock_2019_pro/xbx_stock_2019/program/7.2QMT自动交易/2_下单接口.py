"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

QMT下单接口
"""
import time
from xtquant import xtconstant  # qmt常量
from xtquant.xttype import StockAccount  # 证券账户
from xtquant.xttrader import XtQuantTrader  # 交易接口
import pandas as pd

code = '002389.SZ'

# ========== 初始化交易接口 ==========
path = 'D:\\中航证券QMT实盘-交易端\\userdata_mini'  # 极简版QMT的路径
session_id = 123456  # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号（自己随便写）
xt_trader = XtQuantTrader(path, session_id)  # 创建API实例
user = StockAccount('', 'STOCK')  # 创建股票账户
# 启动交易线程
xt_trader.start()
# 建立交易连接，返回0表示连接成功
connect_result = xt_trader.connect()
print('链接成功' if connect_result == 0 else '链接失败')
# 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
subscribe_result = xt_trader.subscribe(user)
print('订阅成功' if subscribe_result == 0 else '订阅失败')

# ========== 下单流程 ==========

# 查询账户余额
account_res = xt_trader.query_stock_asset(user)
# 将查询到的账户余额数据转为dict
account = {'总资产': account_res.total_asset, '持仓市值': account_res.market_value,
           '可用资金': account_res.cash, '冻结资金': account_res.frozen_cash}
print(account)

# 查询单一股票持仓
single_pos_res = xt_trader.query_stock_position(user, code)
if single_pos_res:  # 若不持有指定的股票，返回None，不会进入if
    # 将查询到的持仓数据数据转为dict
    single_pos = {'证券代码': single_pos_res.stock_code, '成本价': single_pos_res.open_price, '持仓量': single_pos_res.volume,
                  '在途量': single_pos_res.on_road_volume, '可用量': single_pos_res.can_use_volume,
                  '冻结量': single_pos_res.frozen_volume, '昨日持仓量': single_pos_res.yesterday_volume,
                  '市值': single_pos_res.market_value}
    print(f'{code}当前持仓：{single_pos}')
# 查询所有股票持仓
all_pos_res = xt_trader.query_stock_positions(user)
if all_pos_res:  # 若账户空仓，返回None，不会进入if
    pos_list = []
    # 返回的持仓数据需要逐个解析。
    for pos in all_pos_res:
        pos_info = {'证券代码': pos.stock_code, '成本价': pos.open_price, '持仓量': pos.volume, '在途量': pos.on_road_volume,
                    '可用量': pos.can_use_volume, '冻结量': pos.frozen_volume, '昨日持仓量': pos.yesterday_volume,
                    '市值': pos.market_value}
        pos_list.append(pos_info)
    pos_df = pd.DataFrame(pos_list)
    print(f'当前所有持仓：{pos_df}')

# 下单
volume = 200  # 下单量
price = 17  # 下单价格
price_type = xtconstant.FIX_PRICE  # 下单类型
# price_type = 11  # 下单类型
"""
最新价：LATEST_PRICE
指定价/限价：FIX_PRICE
上海最优五档即时成交剩余撤销：MARKET_SH_CONVERT_5_CANCEL
上海最优五档即时成交剩余转限价：MARKET_SH_CONVERT_5_LIMIT
深圳对手方最优价格：MARKET_PEER_PRICE_FIRST
深圳本方最优价格：MARKET_MINE_PRICE_FIRST
深圳即时成交剩余撤销：MARKET_SZ_INSTBUSI_RESTCANCEL
深圳最优五档即时成交剩余撤销：MARKET_SZ_CONVERT_5_CANCEL
深圳全额成交或撤销：MARKET_SZ_FULL_OR_CANCEL
"""
order_id = xt_trader.order_stock(user, code, xtconstant.STOCK_BUY, volume, price_type, price, 'strategy_name', 'remark')
print(f'下单成功，订单号：{order_id}' if order_id != -1 else '下单失败')
time.sleep(2)

# 查询单一订单状态
single_entrust_res = xt_trader.query_stock_order(user, order_id)
single_entrust = {'证券代码': single_entrust_res.stock_code, '下单价格': single_entrust_res.price,
                  '下单量': single_entrust_res.order_volume, '订单状态': single_entrust_res.order_status,
                  '订单标记': single_entrust_res.order_remark, '委托编号': single_entrust_res.order_id,
                  '成交均价': single_entrust_res.traded_price, '成交量': single_entrust_res.traded_volume,
                  '下单时间': single_entrust_res.order_time, '下单类型': single_entrust_res.order_type,
                  '价格类型': single_entrust_res.price_type}
print(f'指定订单结果查询：{single_entrust}')

# 查询所有订单状态
all_entrust_res = xt_trader.query_stock_orders(user)
entrust_list = []
# 返回的委托数据需要逐个解析。
for entrust in all_entrust_res:
    entrust_info = {'证券代码': entrust.stock_code, '下单价格': entrust.price, '下单量': entrust.order_volume,
                    '订单状态': entrust.order_status, '订单标记': entrust.order_remark, '委托编号': entrust.order_id,
                    '成交均价': entrust.traded_price, '成交量': entrust.traded_volume, '下单时间': entrust.order_time,
                    '下单类型': entrust.order_type, '价格类型': entrust.price_type}
    entrust_list.append(entrust_info)
entrust_df = pd.DataFrame(entrust_list)
print(f'今日所有订单订单结果查询：{entrust_df}')

# 撤单，撤回指定的订单。不能一下子全撤
cancel_res = xt_trader.cancel_order_stock(user, order_id)
print(f'撤单成功' if cancel_res != -1 else '撤单失败')

"""
其他用法
除了上述用法之外，部分函数还支持异步。
但是采用异步函数的代码复杂度会直线提升，且运行速度提升不够明显，故不展开讲解。
感兴趣的老板可以自行查看文档中，函数名称带有async字眼的函数。
例如order_stock_async就是order_stock的异步版本。
"""
