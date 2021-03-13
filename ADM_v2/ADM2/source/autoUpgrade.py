#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date      :  2020-09-12
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  autoUpgrade
@Software  :  PyCharm
"""

import os
import time
import shutil
import zipfile
import configparser
from ftplib import FTP
from logger import Logger


def ftpconnect(host, port, username, password):  # 建立ftp连接
    ftp = FTP()
    ftp.set_debuglevel(0)
    ftp.connect(host, int(port))
    ftp.login(username, password)
    return ftp


def downloadfile(ftp, remotepath, localpath):  # 从ftp下载文件
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


def checkVersion(config_file):  # 检查版本
    config = configparser.ConfigParser()
    config.read(config_file)
    value = config['Version']['update']
    return value

def backup_file(abs_path):
    path = [x for x in os.listdir('core') if os.path.isdir(x)]
    if 'backup' in path:
        os.chdir(r'%s\backup' % abs_path)
        backup_path = os.getcwd()
    else:
        backup_path = os.path.join(abs_path, 'backup')
        os.mkdir(backup_path)
    src_file_path = backup_path.replace('backup', 'ADM2')
    backup_filename = ['server_info.csv']
    res_list = []
    for file in backup_filename:
        src_file = src_file_path + '\\' + file
        dst_file = backup_path + '\\' + file
        copy_result = shutil.copy(src_file, dst_file)
        res_list.append(copy_result)
    return res_list, backup_path

def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        raise Exception("非zip压缩文件！")

def copy_file(src_file_path, dst_file_path):
    dst_filename = ['server_info.csv']
    res_list = []
    for file in dst_filename:
        src_file = src_file_path + '\\' + file
        dst_file = dst_file_path + '\\' + file
        copy_result = shutil.copy(src_file, dst_file)
        res_list.append(copy_result)
    return res_list


if __name__ == '__main__':
    print("""***********************ADM2***********************
@ToolsName      :   ADM2
@Version        :   2.0
@Author         :   路宋麟
@Illustration   :   自动化部署监控工具（远程更新版）
**************************************************\n""")
    default_path = os.path.dirname(os.path.realpath(__file__))
    update_filepath = os.path.join(default_path, "update.ini")
    update_conf = configparser.ConfigParser()
    update_conf.read(update_filepath, encoding='utf-8')

    ulog = Logger('update.log', level=update_conf["Log"]["log_level"])

    old_version_dir = os.path.join(default_path, "ADM2")

    try:
        ftp1 = ftpconnect(update_conf['FTP']['ftp_ip'], update_conf['FTP']['ftp_port'],
                         update_conf['FTP']['ftp_user'], update_conf['FTP']['ftp_passwd'])
        if "/" not in update_conf['FTP_FILE']['ftp_chk_file']:
            check_v_filename = update_conf['FTP_FILE']['ftp_chk_file']
        else:
            check_v_filename = update_conf['FTP_FILE']['ftp_chk_file'].split('/')[-1]
        check_v_path = os.path.join(default_path, check_v_filename)
        downloadfile(ftp1, update_conf['FTP_FILE']['ftp_chk_file'], check_v_path)
        update_flag = checkVersion(check_v_path)

        if update_flag == '1':
            ulog.logger.info("检测到新版本...准备更新中...")
            backup_info = backup_file(default_path)
            ulog.logger.info(f"旧版本配置文件备份完毕...备份至：[{backup_info[1]}]")
            ulog.logger.debug(f"旧版本配置文件备份完毕...备份文件响应信息为：{backup_info[0]}")
            shutil.rmtree(old_version_dir)
            ulog.logger.info("旧版本已删除...下载新版本中...")
            ftp2 = ftpconnect(update_conf['FTP']['ftp_ip'], update_conf['FTP']['ftp_port'],
                              update_conf['FTP']['ftp_user'], update_conf['FTP']['ftp_passwd'])

            if "/" not in update_conf['FTP_FILE']['ftp_upgrade_file']:
                zip_filename = update_conf['FTP_FILE']['ftp_upgrade_file']
            else:
                zip_filename = update_conf['FTP_FILE']['ftp_upgrade_file'].split('/')[-1]

            zip_filepath = os.path.join(default_path, zip_filename)
            downloadfile(ftp2, update_conf['FTP_FILE']['ftp_upgrade_file'], zip_filepath)
            unzip_file(zip_filepath, default_path)

            ulog.logger.info("同步配置文件中...")
            recover_config_info = copy_file(os.path.join(default_path, "backup"),os.path.join(default_path, "ADM2"))
            ulog.logger.debug(f"版本更新后已同步旧版配置文件...同步配置文件的响应信息为：\n{recover_config_info}")

            os.remove(check_v_path)
            os.remove(zip_filepath)

            ulog.logger.info("更新完毕...3秒后启动环境检查工具...")
            secs = ['3...', '2...', '1...']
            for i, v in enumerate(secs):
                print(f'{v}')
                if i < len(secs):
                    time.sleep(1)
            print("热身中...请稍等...~")
        else:
            ulog.logger.info("经检测无版本更新...启动环境检查工具中...")
            os.remove(check_v_path)
    except Exception as ex:
        ulog.logger.error(f"错误信息为：{ex}")
    finally:
        os.chdir(old_version_dir)
        os.system("ADM2.exe")

