#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 2:38 下午
# @Author  : jianwei.lv

import baostock as bs
import pandas as pd
import os
from common.os_paths import CSV_PATH

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
# 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
# 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
rs = bs.query_history_k_data_plus("sz.002531",
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2021-11-19', end_date='2021-11-19',
    frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields, index=['天顺风能'])

#### 结果集输出到csv文件 ####
result.to_csv(os.path.join(CSV_PATH, 'test1.csv'), index=False)
result.to_excel(os.path.join(CSV_PATH, 'test1.xlsx'), sheet_name='data')
print(result)

#### 登出系统 ####
bs.logout()