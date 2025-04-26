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
if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
    # 选择日期最新的数据
    df = df.loc[df['选股日期'] == df['选股日期'].max()]
    #  将股票代码保存为数组
    stock_codes = df['股票代码'].values.tolist()
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
    print('选股结果文件不存在')
