#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date      :  2020-02-22
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  clsLrTmp.py
@Software  :  PyCharm
"""
import re
import os
import shutil


if __name__ == '__main__':
    try:
        file_list = []
        file_num = 0
        sysVar = os.environ.get('USERPROFILE')
        tmp_dir = sysVar + r'\AppData\Local\Temp'
        print("清理的目录为： %s" % tmp_dir)
        EXT = [r'brr_+']
        file_list = os.listdir(tmp_dir)  # 列出该目录下的所有文件名
        for f in file_list:
            file_path = os.path.join(tmp_dir, f)  # 将文件名映射成绝对路劲
            if os.path.isdir(file_path):
                for ext in EXT:
                    if re.search(ext, f) is not None:
                        shutil.rmtree(file_path, True)
                        file_num += 1
                        print("已删除LR临时文件目录 : %s" % file_path)
        print("共计删除： %d 临时文件目录" % file_num)
        print("执行完毕！")
    except Exception as ex:
        print('Exception:\r\n')
        print(ex)
    finally:
        os.system("pause")

