#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/22 5:55 下午
# @Author  : jianwei.lv

import datetime

def format_time(t):
    if t==0:
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d')
    elif t!=0 and type(t)==int:
        now = datetime.datetime.now()
        yes = now + datetime.timedelta(days = t)
        return yes.strftime('%Y-%m-%d')

if __name__ == '__main__':
    print(format_time(-1))