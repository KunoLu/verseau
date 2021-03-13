#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date      :  2020-12-05
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  csvTools
@Software  :  PyCharm
"""
import csv


class CsvTools:
    """
    csv 工具读取csv文件获取信息
    """

    def __init__(self, filePath):
        self.filePath = filePath

    def getCsvData(self):
        data = []
        with open(self.filePath) as csvfile:
            # 获取csv数据
            reader = csv.DictReader(csvfile)
            # 将读取每行存入data中
            for row in reader:
                data.append(row)
            return data
