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

        # 前天
        self.qt_time1 = str(format_time_wc(t=-2, start_time=start_time))
        self.qt_time2 = str(format_time_wc(t=-2, start_time=start_time, fm="%Y%m%d"))

    def liangly(self):
        """
        demo
        '两连阴概念板块;2022.11.03涨幅；2日涨幅；2022.11.03换手率; 2022.11.04涨幅; 2022.11.04换手率'
        :return:
        """
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
                          "指数@换手率[{}]".format(self.zt_time2): "昨天换手率",
                          "指数@换手率[{}]".format(self.jt_time2): "当天换手率",
                          "指数@涨跌幅:前复权[{}]".format(self.zt_time2): "昨天涨幅%",
                          "指数@涨跌幅:前复权[{}]".format(self.jt_time2): "今日涨幅%",
                          "指数@区间涨跌幅:不复权[{}]".format(self.zt_time2 + '-' + self.jt_time2): "两日涨幅%"}

        return liangly_question,\
               liangly_colums,\
               liangly_rename

    def sanly(self):
        """
               demo
               '三连阴概念板块;2022.11.02涨幅;2022.11.03涨幅；2022.11.04涨幅;3日涨幅;2022.11.02换手率;2022.11.03换手率;  2022.11.04换手率'
               :return:
        """
        sanly_question = '三连阴概念板块;' + \
                           self.qt_time1 + '涨幅;' + \
                           self.zt_time1+ '涨幅;' + \
                           self.jt_time1 + '涨幅; ' + \
                           '3日涨幅;' + \
                           self.qt_time1 + '换手率; ' + \
                           self.zt_time1 + '换手率; ' + \
                           self.jt_time1 + '换手率' +\
                           self.jt_time1 + '涨幅; ' + \
        """
        demo
        ['code','指数简称','指数@换手率[20221102]','指数@换手率[20221103]','指数@换手率[20221104]','指数@涨跌幅:前复权[20221102]','指数@涨跌幅:前复权[20221103]','指数@涨跌幅:前复权[20221104]','指数@区间涨跌幅:不复权[20221102-20221104]']
        """
        sanly_colums = ['code',
                          '指数简称',
                          '指数@换手率[{}]'.format(self.qt_time2),
                          '指数@换手率[{}]'.format(self.zt_time2),
                          '指数@换手率[{}]'.format(self.jt_time2),
                          '指数@涨跌幅:前复权[{}]'.format(self.qt_time2),
                          '指数@涨跌幅:前复权[{}]'.format(self.zt_time2),
                          '指数@涨跌幅:前复权[{}]'.format(self.jt_time2),
                          '指数@区间涨跌幅:不复权[{}]'.format(self.qt_time2 + '-' + self.jt_time2)]

        """
        demo
        "code": "代码","指数@换手率[20221102]": "前天换手率","指数@换手率[20221103]": "昨天换手率","指数@换手率[20221104]": "当天换手率","指数@涨跌幅:前复权[20221102]": "前天涨幅%","指数@涨跌幅:前复权[20221103]": "昨天涨幅%","指数@涨跌幅:前复权[20221104]": "今日涨幅%","指数@区间涨跌幅:不复权[20221102-20221104]": "三日涨幅%"}
        """
        sanly_rename = {"code": "代码",
                          "指数@换手率[{}]".format(self.qt_time2): "前天换手率",
                          "指数@换手率[{}]".format(self.zt_time2): "昨天换手率",
                          "指数@换手率[{}]".format(self.jt_time2): "当天换手率",
                          "指数@涨跌幅:前复权[{}]".format(self.qt_time2): "前天涨幅%",
                          "指数@涨跌幅:前复权[{}]".format(self.zt_time2): "昨天涨幅%",
                          "指数@涨跌幅:前复权[{}]".format(self.jt_time2): "今日涨幅%",
                          "指数@区间涨跌幅:不复权[{}]".format(self.qt_time2 + '-' + self.jt_time2): "三日涨幅%"}

        return sanly_question, \
               sanly_colums, \
               sanly_rename

if __name__ == '__main__':
    wc=WcManager(start_time="2022.11.04")
    a,b,c = wc.sanly()
    print(c)
