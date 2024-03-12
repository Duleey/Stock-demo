"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

QMT数据接口
"""
import time
from xtquant import xtdata  # 导入qmt库
import pandas as pd

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

"""
订阅：
向服务器订阅指定周期的品种数据，例如1msh600000算一次订阅（最多订阅500次）。
有当日的历史数据，需要更早的，可以使用down_history_data函数下载，3s一次。

可以同时使用全推和订阅
"""

# 指定的股票代码
code = '002389.SZ'

# ========== 订阅数据：和服务器建立链接 ==========
sub_tick_id = xtdata.subscribe_quote(code, 'tick', count=-1)  # 订阅某只股票的tick数据
print('tick数据订阅号：', sub_tick_id)
sub_1min_id = xtdata.subscribe_quote(code, '1m', count=-1)  # 订阅某只股票的1分钟数据，其他的时间格式：5m，1d
print('分钟数据订阅号：', sub_1min_id)
time.sleep(3)

exit()
# 取消订阅
# xtdata.unsubscribe_quote(sub_tick_id)-

# 从内存获取行情数据
mkt_data = xtdata.get_market_data([], [code], 'tick')  # tick数据的格式和1m的数据格式完全不一样
mkt_df = pd.DataFrame(mkt_data[code])
mkt_df['time'] = mkt_df['time'].apply(lambda x: pd.to_datetime(x, unit='ms') + pd.to_timedelta('8H'))  # 时间戳转换为事件格式
print(mkt_df.tail(3), '\n')

# 不断的从内存获取行情数据
print('=' * 10, '开始循环读取最新行情数据', '=' * 10)
count = 0
while count < 10:
    mkt_data = xtdata.get_market_data([], [code], 'tick')  # tick数据的格式和1m的数据格式完全不一样
    mkt_df = pd.DataFrame(mkt_data[code])
    mkt_df['time'] = mkt_df['time'].apply(lambda x: pd.to_datetime(x, unit='ms') + pd.to_timedelta('8H'))  # 时间戳转换为事件格式
    print(mkt_df.tail(3), '\n')
    count += 1
    time.sleep(3)

# 获取财务数据
print('=' * 10, '开始获取财务数据', '=' * 10)
# 需要先下载财务数据，详细见文档xtdata.pdf，Page9
xtdata.download_financial_data([code], ['Balance'])
# 获取财务数，，详细见文档xtdata.pdf，Page9
fin_data = xtdata.get_financial_data([code], ['Balance'], start_time='20201231', end_time='20221231')
fin_df = fin_data[code]['Balance']
print(fin_df)

# 获取交易品种的交易信息，详细见文档xtdata.pdf，Page10
print('=' * 10, '开始获取交易品种的交易信息', '=' * 10)
detail = xtdata.get_instrument_detail(code)
print(detail)

# 获取交易日历：缺陷，获取不到未来的交易日历，详细见文档xtdata.pdf，Page11
print('=' * 10, '开始获取交易日历', '=' * 10)
trading_dates = xtdata.get_trading_dates('SH', start_time='20201231', end_time='20221231')
trading_dates = [pd.to_datetime(date, unit='ms') + pd.to_timedelta('8H') for date in trading_dates]
print(trading_dates[-3:])

# 全推用法，，详细见文档xtdata.pdf，Page4，subscribe_whole_quote
