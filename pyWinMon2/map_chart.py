#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date      :  2020-02-25
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  map_chart.py
@Software  :  PyCharm
"""
import os
import re
import time
import configparser
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 默认不支持负号，需要配置RC参数
        pd.set_option('display.max_columns', None)  # 显示所有列
        pd.set_option('display.max_rows', None)  # 显示所有行
        pd.set_option('max_colwidth', 100)  # 设置value的显示长度为100，默认为50

        default_path = os.path.dirname(os.path.realpath(__file__))
        path = [x for x in os.listdir('.') if os.path.isdir(x)]
        if 'chart' in path:
            pass
        else:
            chartPath = os.path.join(default_path, 'chart')
            os.mkdir(chartPath)

        config_path = os.path.join(default_path, "config.ini")
        conf = configparser.ConfigParser()
        conf.read(config_path)
        interval_sec = int(conf["Default"]["interval_second"])
        if conf["Path"]["abs_path"] == "":
            xls_filename = default_path + "\\" + conf["Default"]["result_filename"]
        else:
            xls_filename = conf["Path"]["abs_path"] + "\\" + conf["Default"]["result_filename"]
        e_file = pd.ExcelFile(xls_filename)
        data = e_file.parse(sheet_index=0)
        title = [column for column in data]

        c_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        pattern = re.compile(r'网络..流量')
        for i in range(1, len(title)):
            x = data.loc[:, '时间戳']  # loc利用标签来获得行列
            y = data.loc[:, title[i]]
            plt.plot(x, y, label=title[i], c='red')
            plt.xticks(rotation=45)  # x轴字体旋转角度设置
            plt.xlabel('时间戳')
            match = pattern.match(title[i])
            if match:
                plt.ylabel('单位：MB')
            else:
                plt.ylabel('单位：%')
                plt.ylim(ymin=0, ymax=100)
            name_split = title[i].split("(")
            chartName = name_split[0] + '_' + c_time
            plt.title(title[i])
            plt.legend()
            chart_file = default_path + "\\chart\\" + chartName
            plt.savefig(r'%s.jpg' % chart_file)
            plt.clf()  # 重置画布，否则后续图表生成，图表数据依次叠加
        print("Complete!")
    except Exception as ex:
        print('Exception:\r\n')
        print(ex)
    finally:
        os.system("pause")
