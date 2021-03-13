#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date      :  2021-02-12
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  Logger
@Software  :  PyCharm
"""

import sys
import logging
from logging import handlers


class Logger(object):

    def __init__(self, filename, level='info'):
        # 日志级别关系映射
        self.level_relations = {
            'debug': logging.DEBUG,
            'DEBUG': logging.DEBUG,
            'info': logging.INFO,
            'INFO': logging.INFO,
            'warning': logging.WARNING,
            'WARNING': logging.WARNING,
            'error': logging.ERROR,
            'ERROR': logging.ERROR,
            'critical': logging.CRITICAL,
            'CRITICAL': logging.CRITICAL
        }
        # 日志文件名（带路径）
        self.filename = filename
        # 日志级别
        self.level = level
        # 获取logger实例，如果参数为空则返回root logger
        self.logger = logging.getLogger(filename)

    def get_logger(self, when='D', backCount=3,
                   fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        logger = self.logger
        # 设置日志格式
        format_str = logging.Formatter(fmt)
        # 设置日志级别
        logger.setLevel(self.level_relations.get(self.level))
        # 往屏幕上输出
        # sh = logging.StreamHandler(sys.stdout)
        # 设置屏幕上显示的格式
        # sh.setFormatter(format_str)
        # 配置备份日志
        th = handlers.TimedRotatingFileHandler(filename=self.filename, when=when, backupCount=backCount,
                                               encoding='utf-8')
        # 设置文件里写入的格式
        th.setFormatter(format_str)
        # 为logger添加的日志处理器
        # logger.addHandler(sh)
        logger.addHandler(th)

        return logger
