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

def format_time_wc(t=0, start_time=None, fm="%Y.%m.%d"):
    if start_time == None:
        now = datetime.datetime.now()
    elif start_time != None:
        try:
            now = datetime.datetime.strptime(start_time, fm)
        except ValueError as e:
            n_start_time = start_time.replace('.', '')
            now = datetime.datetime.strptime(n_start_time, fm)
    yes = now + datetime.timedelta(days=t)
    return yes.strftime(fm)


if __name__ == '__main__':
    print(format_time_wc(-1, start_time="2022.10.30"))
    print(datetime.datetime.now())