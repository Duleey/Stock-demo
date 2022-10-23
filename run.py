#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/22 7:53 下午
# @Author  : jianwei.lv

from common.stock_manager import StockManager
from util.stock_sizer import Sizer
import pandas as pd
import common.os_paths as path
import os

s = Sizer()
sm = StockManager()

sm.stock_list = sm.s_list
new_list = []

for i in sm.stock_list:
    res = s.if_turndown_oc(code=str(i), t=-3)
    new_list.append(res)

result = pd.DataFrame(new_list, columns=["code"])
result.to_excel(os.path.join(path.CSV_PATH, 'runtest'+'.xls'), encoding="gbk", index=False)

