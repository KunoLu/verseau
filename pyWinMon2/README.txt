# 执行脚本前，请先修改config.ini配置文件！

# pyWinMon2.py脚本使用模块为：(windows系统资源监控脚本)
import os
import time
import psutil
import datetime
import configparser
from xlrd import open_workbook
from xlutils.copy import copy
# 除xlrd、xlutils模块，其他均为python自带模块


# map_chart.py脚本使用模块为：(分析结果制图脚本)
import os
import re
import time
import configparser
import pandas as pd
import matplotlib.pyplot as plt
# pandas、matplotlib模块，其他均为python自带模块


# 如本地尚未安装对应模块，则在cmd中python -m pip install [模块名]远程在线下载安装即可；
# 或离线安装pyWinMon2\offlineLib文件夹下的"*.whl"文件


# config.ini配置文件：(以上两脚本共用文件！执行脚本前请先修改config.ini文件！)
# 间隔秒数：interval_second; 循环次数：cycle_times; 结果文件名：result_filename;
# 结果文件名建议不修改，如需修改请确保路径下的xls结果文件名与修改后的保持一致，否则报错！
[Default]
interval_second=1
cycle_times=3
result_filename=res_data_pyWinMon2.xls


# 结果文件的绝对路径：abs_path; 该选项为空时默认获取脚本的当前路径；
# 如修添加该路径，请自行复制xls文件至修改的路径下，否则报错！
[Path]
abs_path=


# 使用说明：
# 在Windows下调用格式为：
# python pyWinMon2.py
# python map_chart.py
# 或双击pyWinMon2.exe、map_chart.exe