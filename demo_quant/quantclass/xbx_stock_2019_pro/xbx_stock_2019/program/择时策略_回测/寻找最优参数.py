"""
《邢不行-2019新版|Python股票量化投资课程》
author：邢不行
微信：xingbuxing0807

通过循环，寻找择时策略的最优参数
"""
from demo_quant.quantclass.xbx_stock_2019_pro.xbx_stock_2019.program.择时策略_回测.Functions import cal_fuquan_price, cal_zdt_price
from demo_quant.quantclass.xbx_stock_2019_pro.xbx_stock_2019.program.择时策略_回测.Signals import simple_moving_average_signal,simple_moving_average_para_list
from demo_quant.quantclass.xbx_stock_2019_pro.xbx_stock_2019.program.择时策略_回测.Position import position_at_close
from demo_quant.quantclass.xbx_stock_2019_pro.xbx_stock_2019.program.择时策略_回测.Evaluate import equity_curve_with_long_at_close
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 读入股票数据
stock_code = 'sz000002'
df = pd.read_csv('/Users/xingbuxingx/Desktop/股票量化课程/xbx_stock_2019/data/择时策略-回测/%s.csv' % stock_code,
                 encoding='gbk', skiprows=1, parse_dates=['交易日期'])
df.sort_values(by=['交易日期'], inplace=True)
df.drop_duplicates(subset=['交易日期'], inplace=True)
df.reset_index(inplace=True, drop=True)


# 计算复权价格、涨停价格
df = cal_fuquan_price(df, fuquan_type='后复权')
df = cal_zdt_price(df)


# 构建策略参数遍历范围
para_list = simple_moving_average_para_list(ma_short=range(10, 200, 10), ma_long=range(10, 200, 10))


# 遍历参数
rtn = pd.DataFrame()
for para in para_list:
    # 计算策略交易信号，此处df需要copy
    temp_df = simple_moving_average_signal(df.copy(), para=para)

    # 计算实际持仓
    temp_df = position_at_close(temp_df)

    # 选择时间段
    # 截取上市一年之后的数据
    temp_df = temp_df.iloc[250 - 1:]  # 股市一年交易日大约250天
    # 截取2007年之后的数据
    temp_df = temp_df[temp_df['交易日期'] >= pd.to_datetime('20070101')]  # 一般可以从2006年开始

    # 计算资金曲线
    temp_df = equity_curve_with_long_at_close(temp_df, c_rate=2.5/10000, t_rate=1.0/1000, slippage=0.01)

    # 计算收益
    equity_curve = temp_df.iloc[-1]['equity_curve']
    equity_curve_base = temp_df.iloc[-1]['equity_curve_base']
    print(para, '策略最终收益：', equity_curve)

    rtn.loc[str(para), 'equity_curve'] = equity_curve
    rtn.loc[str(para), 'equity_curve_base'] = equity_curve_base

print(rtn.sort_values(by='equity_curve', ascending=False))
