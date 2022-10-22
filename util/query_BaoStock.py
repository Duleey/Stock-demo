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
        logging.info('login respond code:' + lg.error_code)
        logging.info('login respond msg:' + lg.error_msg)

    #详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    #分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    #周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    def get_kline_data(self,
                       #### 获取历史k线数据 ####
                       code="sz.002531",
                       fields="date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
                       start_time='2021-11-19',
                       end_time='2021-11-19',
                       frequency='d',
                       adjustflag='2'):
        self.rs = bs.query_history_k_data_plus(code=code,
                                          fields=fields,
                                          start_date=start_time,
                                          end_date=end_time,
                                          frequency=frequency,
                                          adjustflag=adjustflag)
        logging.info('query_history_k_data_plus respond code:' + self.rs.error_code)
        logging.info('query_history_k_data_plus respond msg:' + self.rs.error_msg)
        return self.rs

    def print_rs(self):
        #### 打印结果 ####
        data_list = []
        while (self.rs.error_code == '0') & self.rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(self.rs.get_row_data())
        return data_list

    def get_data(self, data, doc="c", name="basic"):
        #### 写入文件 ####
        result = pd.DataFrame(data, columns=self.rs.fields)
        if doc == "c":
            result.to_csv(os.path.join(path.CSV_PATH, name+'.csv'), encoding="gbk", index=False)
            logging.info("to_esv success to {}".format(os.path.join(path.CSV_PATH, name+'.csv')))
        elif doc == "e":
            result.to_excel(os.path.join(path.CSV_PATH, name+'.xls'), encoding="gbk", index=False)
            logging.info("to_esv success to {}".format(os.path.join(path.CSV_PATH, name+'.xls')))

    def LogOut(self):
        bs.logout()

if __name__ == '__main__':
    s = QueryBaoStock()
    res = s.get_kline_data()
    datalist = s.print_rs()
    s.get_data(data=datalist)
    s.LogOut()