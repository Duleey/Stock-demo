#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 4:35 下午
# @Author  : jianwei.lv

stock_list = ['sz']

class StockManager:

    __stock_list = []

    @property
    def stock_list(self):
        return __stock_list

    @stock_list.setter
    def stock_list(self, value):
        self.__stock_list = value

if __name__ == '__main__':
    sm = StockManager
    # sm.stock_list = 123
    print(sm.stock_list)