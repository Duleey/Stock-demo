#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/21 3:57 下午
# @Author  : jianwei.lv

import os
import time

# 通过当前文件的绝对路径，其父级目录一定是框架的base目录，然后确定各层的绝对路径。
BASE_PATH = os.path.dirname(os.path.dirname((__file__)))
CSV_PATH = os.path.join(BASE_PATH, 'CSV')
LOG_PATH = os.path.join(BASE_PATH, 'log')



t1 = time.strftime("%Y_%m_%d_%H_%M")

print(BASE_PATH)
print(CSV_PATH)
print(LOG_PATH)