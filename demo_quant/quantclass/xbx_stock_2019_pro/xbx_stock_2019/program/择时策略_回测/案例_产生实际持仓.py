"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

通过一个简单的案例策略，来演示如何将策略signal转换为实际仓位
"""
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 99999)  # 最多显示数据的行数
pd.set_option('display.max_columns', 99999)


# ===导入数据
df = pd.read_hdf(
    '/Users/lvjianwei/Desktop/workspace/stock/Stock-demo/demo_quant/quantclass/xbx_stock_2019_pro/xbx_stock_2019/data/择时策略-回测/signals.h5',
    key='df')

# ===由signal计算出实际的每天持有仓位
# 在产生signal的k线结束的时候，进行买入
df['signal'].fillna(method='ffill', inplace=True)
df['signal'].fillna(value=0, inplace=True)  # 将，始行数的signal补全为0
df['pos'] = df['signal'].shift()
df['pos'].fillna(value=0, inplace=True)  # 将初始行数的pos补全为0

# ===对涨跌停无法买卖做出相关处理。
# 找出收盘价无法买入的K线
cannot_buy_condition = df['收盘价'] >= df['涨停价']
# 将找出上一周期无法买入的K线、并且signal为1时，的'pos'设置为空值
df.loc[cannot_buy_condition.shift() & (df['signal'].shift() == 1), 'pos'] = None  # 2010-12-22

# 找出收盘价无法卖出的K线
cannot_sell_condition = df['收盘价'] <= df['跌停价']
# 将找出上一周期无法卖出的K线、并且signal为0时的'pos'设置为空值
df.loc[cannot_sell_condition.shift() & (df['signal'].shift() == 0), 'pos'] = None

# pos为空的时，不能买卖，只能和前一周期保持一致。
df['pos'].fillna(method='ffill', inplace=True)


# ===如果是分钟级别的数据，还需要对t+1交易制度进行处理，在之后案例中进行演示


# ===删除无关中间变量
df.drop(['signal'], axis=1, inplace=True)


# ===将数据存入hdf文件中
df.to_hdf(
    '/Users/lvjianwei/Desktop/workspace/stock/Stock-demo/demo_quant/quantclass/xbx_stock_2019_pro/xbx_stock_2019/data/择时策略-回测/pos.h5',
    key='df', mode='w')
