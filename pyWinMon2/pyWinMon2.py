#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date      :  2020-02-20
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  pyWinMon2.py
@Software  :  PyCharm
"""

import os
import time
import psutil
import datetime
import configparser
from xlrd import open_workbook
from xlutils.copy import copy


# 监控CPU信息
def cpu():
    cpu = psutil.cpu_count(False)  # cpu核数 默认逻辑CPU核数， False查看真实cpu核数
    cpu_per = psutil.cpu_percent(1)  # 每秒cpu使用率，（1，true） 每一核cpu的每秒使用率
    # print(cpu, cpu_per)
    return cpu_per


# 监控内存信息
def mem():
    mem = psutil.virtual_memory()  # 查看内存信息:(total,available,percent,used,free)
    # print(mem)
    mem_total = round(mem.total / 1024 / 1024 / 1024, 2)  # GB
    mem_used = round(mem.used / 1024 / 1024 / 1024, 2)
    mem_per = mem.percent
    mem_info = {
        'mem_total': mem_total,
        'mem_used': mem_used,
        'mem_per': mem_per,
    }
    return mem_info


# 监控磁盘使用率
def disk():
    disk_id = []
    disk_total = []
    disk_used = []
    disk_free = []
    disk_percent = []
    disk_sum = {}
    for id in psutil.disk_partitions():
        if 'cdrom' in id.opts or id.fstype == '':
            continue
        disk_name = id.device.split(':')
        s = disk_name[0]
        disk_id.append(s)
        disk_info = psutil.disk_usage(id.device)
        disk_total.append(disk_info.total)
        disk_used.append(disk_info.used)
        disk_free.append(disk_info.free)
        disk_percent.append(disk_info.percent)
    for i in range(len(disk_id)):
        disk_sum[disk_id[i]] = disk_percent[i]
    return disk_sum


# 监控网络流量
def network():
    # 查看网络流量的信息；(bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)
    network = psutil.net_io_counters()
    network_in = round(psutil.net_io_counters().bytes_recv / 1024 / 1024, 2)  # 每秒接受的MB
    network_out = round(psutil.net_io_counters().bytes_sent / 1024 / 1024, 2)
    network_info = {
        'network_in': network_in,
        'network_out': network_out
    }
    return network_info


# 间隔一定时间，输出当前的CPU状态信息
def all_msg():
    msg = []
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # append之后是['2019-03-21 15:31:39']
    msg.append(now_time)  # 获取时间点
    cpu_info = cpu()
    msg.append(cpu_info)  # cpu 使用率,单位：%
    mem_info = mem()
    msg.append(mem_info['mem_per'])  # 内存使用率,单位：%
    network_info = network()
    msg.append(network_info['network_out'])  # 网络流量发送的量（MB）
    msg.append(network_info['network_in'])  # 网络流量接收的量（MB）
    disk_sum = disk()
    for key in disk_sum:
        msg.append(disk_sum[key])  # 磁盘使用率，单位：%
    return msg


def write_xls(lis, times, filename):
    rb = open_workbook(filename)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    ws.write(0, 0, '时间戳')
    ws.write(0, 1, 'CPU(%)')
    ws.write(0, 2, '内存(%)')
    ws.write(0, 3, '网络发送流量(MB)')
    ws.write(0, 4, '网络接收流量(MB)')
    disk_sum = disk()
    describe = '磁盘使用率(%)'
    index_y = 4
    for key in disk_sum:
        index_y += 1
        total_des = key + describe
        ws.write(0, index_y, total_des)
    for i in range(0, len(lis)):
        ws.write(times, i, lis[i])
    wb.save(filename)


if __name__ == '__main__':
    try:
        default_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(default_path, "config.ini")
        conf = configparser.ConfigParser()
        conf.read(config_path)
        sec = int(conf["Default"]["interval_second"])
        total_times = int(conf["Default"]["cycle_times"])
        if conf["Path"]["abs_path"] == "":
            res_file = default_path + "\\" + conf["Default"]["result_filename"]
        else:
            res_file = conf["Path"]["abs_path"] + "\\" + conf["Default"]["result_filename"]

        str_list = []
        describe = '磁盘使用率(%)'
        title = ["时间戳", "CPU(%)", "内存(%)", "网络发送的流量(MB)", "网络接收的流量(MB)"]
        disk_sum = disk()
        for key in disk_sum:
            total_des = key + describe
            str_list.append(total_des)
        for var in range(len(str_list)):
            title.append(str_list[var])
        print(title)

        cnt_times = 1
        while (1):
            msg = all_msg()
            print(msg)  # 实时打印每隔sec秒写入excel的数据。
            write_xls(msg, cnt_times, res_file)
            cnt_times += 1
            # 每隔sec秒，统计一次当前计算机的使用情况。
            time.sleep(sec)
            # 统计了total_times次后跳出当前循环
            if (cnt_times > total_times):
                break
    except Exception as ex:
        print('Exception:\r\n')
        print(ex)
    finally:
        os.system("pause")

"""
# 发邮件进行实时报告计算机的状态
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from email.header import Header
def send_email(info):
    sender = '***@qq.com'
    recevier = '***@qq.com'
    subject = 'Warning'
    username = '***@qq.com'
    password = '***'  # 相应的密码
    msg = MIMEText(info, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = recevier
    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com')
    smtp.login(username, password)
    smtp.sendmail(sender, recevier, msg.as_string())
    smtp.quit()
# 主函数调用，调用其他信息
def main():
    cpu_info = cpu()
    mem_info = mem()
    disk_info = disk()
    network_info = network()
    info = ''' 
                监控信息 
        ========================= 
        cpu使用率： : %s,
        ========================= 
        内存总大小（MB） : %s, 
        内存使用大小（MB） : %s, 
        内存使用率 : %s,
        =========================
        C盘使用率: %s, 
        D盘使用率: %s,
        E盘使用率: %s,
        =========================
        网络流量接收的量（MB） : %s, 
        网络流量发送的量（MB）: %s,
    ''' % (cpu_info,
          mem_info['mem_total'], mem_info['mem_used'], mem_info['mem_per'],
          disk_info['c_per'], disk_info['d_per'], disk_info['e_per'],
          network_info['network_sent'], network_info['network_recv'])
    send_email(info)
main()
"""
