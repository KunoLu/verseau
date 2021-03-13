#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date      :  2020-12-05
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  test
@Software  :  PyCharm
"""
import os
import re

# default_path = os.path.dirname(os.path.realpath(__file__))
# dst_path = default_path.replace('core', 'conf')
# configFileName = dst_path + '\pstat_server_info.csv'
#
# print(f"{default_path}\n{dst_path}\n{configFileName}")

def alter(file, old_str, new_str):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def change_pstat_mon_time():
    str = "self.time = 93600"
    res = re.search('self.time = (\d+)', str).group()
    print(res)