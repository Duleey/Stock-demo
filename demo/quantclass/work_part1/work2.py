#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/12 5:26 下午
# @Author  : jianwei.lv

"""
获取上证指数日线数据，数据截止日期为最近的交易日，数据条数不少于200条
"""

from random import randint
import requests, os, json, re,datetime,time
import pandas as pd

index_list = ['sh000001']
all_data_path = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'

}
for index in index_list:
    print(index)
    url = 'https://proxy.finance.qq.com/ifzqgtimg/appstock/app/newfqkline/get'
    start_time = '1900-01-01'
    end_time = ''
    df_list = []
    while True:
        params = {
            '_var': 'kline_dayqfq',
            'param': f'{index},day,{start_time},{end_time},2000,qfq',
            'r': f'0.{randint(10 ** 15, (10 ** 16) - 1)}',
        }
        res = requests.get(url, params=params, headers=headers)
        res_json = json.loads(re.findall('kline_dayqfq=(.*)', res.text)[0])
        if res_json['code'] == 0:
            _df = pd.DataFrame(res_json['data'][index]['day'])
            df_list.append(_df)
            if _df.shape[0] <= 1:
                break
            end_time = _df.iloc[0][0]
        time.sleep(2)
    df = pd.concat(df_list, ignore_index=True)
    # ===对数据进行整理
    rename_dict = {0: 'candle_end_time', 1: 'open', 2: 'close', 3: 'high', 4: 'low', 5: 'amount', 6: 'info'}
    # 其中amount单位是手，说明数据不够精确
    df.rename(columns=rename_dict, inplace=True)
    df['candle_end_time'] = pd.to_datetime(df['candle_end_time'])
    df.drop_duplicates('candle_end_time', inplace=True)  # 去重
    df.sort_values('candle_end_time', inplace=True)
    df['candle_end_time'] = df['candle_end_time'].dt.strftime('%Y-%m-%d')
    if 'info' not in df:
        df['info'] = None
    df = df[['candle_end_time', 'open', 'high', 'low', 'close', 'amount', 'info']]
    start = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + '9:30'
    start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M")

    end = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + '15:00'
    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M")
    to_csv_path = all_data_path
    if not os.path.exists(to_csv_path):  # 判断文件夹是否存在
        os.makedirs(to_csv_path)  # 不存在则创建
    df.to_csv(to_csv_path + '/%s.csv' % index, index=False, encoding='gbk')
