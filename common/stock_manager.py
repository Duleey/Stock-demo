#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 4:35 下午
# @Author  : jianwei.lv

class StockManager:

    s_list = ['sz.000595', 'sz.000534']

    @property
    def stock_list(self):
        return self.__stock_list

    @stock_list.setter
    def stock_list(self, value):
        self.__stock_list = value

if __name__ == '__main__':
    sm = StockManager
    sm.stock_list = sm.s_list
    print(sm.stock_list)