#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 11:37 下午
# @Author  : jianwei.lv

import wencai as wc

# 若需中文字段则cn_col=True,chromedriver路径不在根目录下需指定execute_path
wc.set_variable(cn_col=True)
wc.search('1')