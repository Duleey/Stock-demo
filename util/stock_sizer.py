#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/22 5:44 下午
# @Author  : jianwei.lv

from util.query_BaoStock import QueryBaoStock
from common.format_time import format_time

# if res[-3][-1] > res[-2][-1] > res[-1][-1]:
#     new_list = []
#     for i in res:
#         if i[1] not in new_list:
#             new_list.append(i[1])
#     print(new_list)

class Sizer:
    def __init__(self):
        self.qbs = QueryBaoStock()

    # 缩量、连续阴线
    """
    code:股票代码
    t: -2为两连阴，-3为三连阴，默认-3
    判断是否连阴符合条件
    :return code
    """
    def if_turndown_oc(self, code, t=-3):
        self.qbs.get_kline_data(code=code,
                           start_time=format_time(t), end_time=format_time(0),
                           fields="date,code,open,close,volume,turn")
        res = self.qbs.print_rs()
        # 三连阴情况
        if t == -3:
            if res[0][2] > res[0][3] \
                    and res[1][2] > res[1][3] \
                    and res[2][2] > res[2][3] \
                    and res[-3][-1] > res[-2][-1] > res[-1][-1]:
                return res[0][1]

        # 两连阴情况
        if t == -2:
            if res[0][2] > res[0][3] \
                    and res[1][2] > res[1][3] \
                    and res[-2][-1] > res[-1][-1]:
                return res[0][1]

if __name__ == '__main__':
    s = Sizer()
    res = s.if_turndown_oc(code='sz.000595', t=-3)
    print(res)
