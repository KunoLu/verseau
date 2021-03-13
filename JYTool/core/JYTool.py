#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date      :  2021-02-27
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  JYTool
@Software  :  PyCharm
"""

import json
import yaml
import pysnooper
import traceback
import PySimpleGUI as sg
from functools import wraps
from core.api.Logger import Logger


def logging_decorator(func):
    @wraps(func)
    def log(*args, **kwargs):
        try:
            Logger(r"../logs/run.log").get_logger().info("Function is : {}({}, {})".format(func.__name__, args, kwargs))
            return func(*args, **kwargs)

        except Exception:
            Logger(r"../logs/run.log").get_logger().error(
                f"{func.__name__} is error,here are details:{traceback.format_exc()}")

    return log


@logging_decorator
@pysnooper.snoop(output=r'../logs/snoop.log', overwrite=False, prefix='func_j2y ')
def j2y(json_abspath, yaml_abspath):
    try:
        # 读取json文件内容并转换成字典
        with open(json_abspath, 'r', encoding='utf-8') as fj:
            dict_json = json.load(fj)

        # 字典转换成yaml格式字符串并写入yaml文件
        with open(yaml_abspath, "w", encoding='utf-8') as fy:
            yaml.dump(dict_json, fy)

    except Exception as ex:
        return ex


@logging_decorator
@pysnooper.snoop(output=r'../logs/snoop.log', overwrite=False, prefix='func_y2j ')
def y2j(yaml_abspath, json_abspath):
    try:
        # 读取yaml文件内容并转换成字典
        with open(yaml_abspath, 'r', encoding='utf-8') as fy:
            dict_yaml = yaml.load(fy, Loader=yaml.FullLoader)

        # 把字典转换成json字符串并存储在文件中
        with open(json_abspath, "w", encoding='utf-8') as fj:
            json.dump(dict_yaml, fj, indent=2, ensure_ascii=False)

    except Exception as ex:
        return ex


@logging_decorator
@pysnooper.snoop(output=r'../logs/snoop.log', overwrite=False, prefix='func_sg_process ')
def sg_process(src_format: str, dst_format: str, ):
    try:
        # GUi界面的流程逻辑
        src_file_path = sg.popup_get_file(title='选择文件',
                                          message=f'请选择{src_format}格式文件！',
                                          default_extension=f'{src_format.lower()}',
                                          file_types=((f"{src_format} Files", f"*.{src_format.lower()}"),),
                                          keep_on_top=True,
                                          initial_folder=r'../conf/')

        if src_file_path != None:
            dst_file_path = sg.popup_get_file(title='保存文件',
                                              message=f'请保存{dst_format}格式文件！',
                                              save_as=True,
                                              default_extension=f'{dst_format.lower()}',
                                              file_types=((f"{dst_format} Files", f"*.{dst_format.lower()}"),),
                                              keep_on_top=True,
                                              initial_folder=r'../conf/')

            sg.popup_scrolled(f'生成的{dst_format}格式文件路径为：\n{dst_file_path}', title='result', size=(80, 10))

        else:
            dst_file_path = None

        return src_file_path, dst_file_path

    except Exception as ex:
        return ex


@logging_decorator
@pysnooper.snoop(output=r'../logs/snoop.log', overwrite=False, prefix='func_main ')
def main():
    try:
        choose = sg.popup(title='JYTool', custom_text=('JSON转YAML', 'YAML转JSON'), keep_on_top=True, auto_close=True,
                          auto_close_duration=10)

        if choose == 'JSON转YAML':
            j2y_json_file_path, j2y_yaml_file_path = sg_process('JSON', 'YAML')
            j2y(j2y_json_file_path, j2y_yaml_file_path)

        elif choose == 'YAML转JSON':
            y2j_yaml_file_path, y2j_json_file_path = sg_process('YAML', 'JSON')
            y2j(y2j_yaml_file_path, y2j_json_file_path)

    except Exception as ex:
        return ex


if __name__ == '__main__':
    # 执行main方法
    main()
