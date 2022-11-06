#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 4:35 下午
# @Author  : jianwei.lv

from common.format_time import format_time_wc

class WcManager:
    def __init__(self, start_time=None):
        # 昨天
        self.zt_time1 = str(format_time_wc(t=-1, start_time=start_time))
        # 今日
        self.jt_time1 = str(format_time_wc(t=0, start_time=start_time))

        # 昨天
        self.zt_time2 = str(format_time_wc(t=-1, start_time=start_time, fm="%Y%m%d"))
        # 今日
        self.jt_time2 = str(format_time_wc(t=0, start_time=start_time, fm="%Y%m%d"))


    def liangly(self):
        liangly_question = '两连阴概念板块;' +\
                           self.zt_time1 + '涨幅;'+\
                           '2日涨幅;' +\
                           self.zt_time1 + '换手率; '+\
                           self.jt_time1 +'涨幅; ' +\
                           self.jt_time1 +'换手率'\

        """
        demo
        ['code','指数简称','指数@换手率[20221103]','指数@换手率[20221104]','指数@涨跌幅:前复权[20221103]','指数@涨跌幅:前复权[20221104]','指数@区间涨跌幅:不复权[20221103-20221104]']
        """
        liangly_colums = ['code',
                          '指数简称',
                          '指数@换手率[{}]'.format(self.zt_time2),
                          '指数@换手率[{}]'.format(self.jt_time2),
                          '指数@涨跌幅:前复权[{}]'.format(self.zt_time2),
                          '指数@涨跌幅:前复权[{}]'.format(self.jt_time2),
                          '指数@区间涨跌幅:不复权[{}]'.format(self.zt_time2 + '-' + self.jt_time2)]

        """
        demo
        "code": "代码","指数@换手率[20221103]": "前一天换手率","指数@换手率[20221104]": "当天换手率","指数@涨跌幅:前复权[20221103]": "前一天涨幅%","指数@涨跌幅:前复权[20221104]": "今日涨幅%","指数@区间涨跌幅:不复权[20221103-20221104]": "两日涨幅%"}
        """
        liangly_rename = {"code": "代码",
                          "指数@换手率[{}]".format(self.zt_time2): "前一天换手率",
                          "指数@换手率[{}]".format(self.jt_time2): "当天换手率",
                          "指数@涨跌幅:前复权[{}]".format(self.zt_time2): "前一天涨幅%",
                          "指数@涨跌幅:前复权[{}]".format(self.jt_time2): "今日涨幅%",
                          "指数@区间涨跌幅:不复权[{}]".format(self.zt_time2 + '-' + self.jt_time2): "两日涨幅%"}

        return liangly_question,\
               liangly_colums,\
               liangly_rename

if __name__ == '__main__':
    wc=WcManager(start_time="2022.11.04")
    a,b,c = wc.liangly()
    print(c)
