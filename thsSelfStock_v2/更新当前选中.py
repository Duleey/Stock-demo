import os
import pandas as pd
from core.model.backtest_config import load_config
from operate import add_stock_to_custom_block
from operate import new_custom_block
from operate import delete_custom_block
from config_ths import add_signal

mode = 'cover'  # 写入模式，cover 覆盖，append 追加
conf = load_config()
# 选股结果 CSV 文件路径
csv_file_path = f"{conf.get_result_folder()}/选股结果.csv"
period_offset = pd.read_csv(conf.period_offset_path, skiprows=1, encoding='gbk')
period_offset['交易日期'] = pd.to_datetime(period_offset['交易日期'])
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df['选股日期'] = pd.to_datetime(df['选股日期'])
    #  将股票代码保存为数组
    stock_codes = []
    offset_list = df['持仓周期'].unique()
    today = pd.to_datetime('today').strftime('%Y/%m/%d')
    for offset in offset_list:
        # 因为有周末和假期，所以选取距离今天最近的交易日
        offset_num = period_offset.loc[period_offset['交易日期'] <= today, offset].values[-1]
        # 在选股周期的前一天选出股票，所以需要减一天
        days = period_offset.loc[period_offset[offset] == offset_num, '交易日期'].values - pd.Timedelta(days=1)
        # 取出在对应日期内的选股结果
        codes = df[(df['选股日期'].isin(days)) & (df['持仓周期'] == offset)]['股票代码'].values
        stock_codes.extend(codes)
    # stock_codes去重
    stock_codes = list(set(stock_codes))
    if len(stock_codes) == 0:
        print('最近交易周期没有选出股票')
        exit()
    if mode == 'cover':
        try:
            delete_custom_block(conf.name + add_signal)
        except Exception as e:
            # 捕获其他异常并打印错误信息
            print('不存在自定义板块，直接创建')
        new_custom_block(conf.name + add_signal, stock_codes)
        add_stock_to_custom_block(conf.name + add_signal, stock_codes)
        print('已成功覆盖自定义板块', conf.name + add_signal, stock_codes)
    elif mode == 'append':
        new_custom_block(conf.name + add_signal, stock_codes)
        add_stock_to_custom_block(conf.name + add_signal, stock_codes)
        print('已成功追加股票至自定义板块', conf.name + add_signal, stock_codes)
    else:
        print('写入模式错误，请选择 cover 或 append')
else:
    print('选股结果文件不存在')
