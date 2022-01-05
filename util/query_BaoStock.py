#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 5:09 下午
# @Author  : jianwei.lv

import baostock as bs
import pandas as pd
import os
import common.os_paths as path
from common.logger import Logger

logging = Logger()
class QueryBaoStock:
    def __init__(self):
        #### 登陆系统 ####
        lg = bs.login()
        # 显示登陆返回信息
        logging.info('login respond error_code:' + lg.error_code)
        logging.info('login respond  error_msg:' + lg.error_msg)

    def get_kline_data(self):
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
        rs = bs.query_history_k_data_plus("sz.002531",
                                          "date,code,open,high,low,close,preclose,volumgit remote add origin git@github.com:Duleey/Stock-demo.gite,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                          start_date='2021-11-19', end_date='2021-11-19',
                                          frequency="d", adjustflag="3")
        logging.info('query_history_k_data_plus respond error_code:' + rs.error_code)
        logging.info('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    def LogOut(self):
        bs.logout()

if __name__ == '__main__':
    s = QueryBaoStock()
    s.get_kline_data()