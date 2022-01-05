#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/5 10:18 下午
# @Author  : jianwei.lv

import logging, os, datetime
from common.os_paths import LOG_PATH

now_time = datetime.datetime.now()
now_time.strftime('%Y%m%d')

# todo 日志名字跟着类名
# todo 日志后缀优化，不要小数点 .123123123

class Logger:
    def __init__(self, clevel=logging.DEBUG, Flevel=logging.DEBUG,
                 path=os.path.join(LOG_PATH, 'log' + str(now_time) + '.log')):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

if __name__ =='__main__':
     logyyx = Logger(logging.DEBUG, logging.DEBUG)
     logyyx.debug('一个debug信息')
     logyyx.info('一个info信息')
     logyyx.warn('一个warning信息')
     logyyx.error('一个error信息')
     logyyx.cri('一个致命critical信息')