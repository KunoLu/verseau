#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date      :  2020-12-05
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  ADM2
@Software  :  PyCharm
"""
import os
import multiprocessing
from csvTools import CsvTools
from RST import RemoteServerTools


def autoStartMini2(ip, username, password, port, local_path, remote_path, start_path, init_server_kind,
                   dst_server_kind):
    # 获取远端路径及文件名
    (remote_path1, fileName) = os.path.split(remote_path)
    print('ip={} remote_path ={} fileName={}\n上传中...'.format(ip, remote_path1, fileName))
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ftp连接
    remoteTools.ftpConnect()
    # 3.创建ssh连接
    remoteTools.connect()
    # 4.上传脚本文件
    remoteTools.upLoad(remote_path, local_path)
    # 5.unzip remote_path
    remoteTools.run_cmd('cd {} && tar -xf {}'.format(remote_path1, fileName))
    # 6.删除zip文件
    remoteTools.run_cmd('cd {} && rm -rf {}'.format(remote_path1, fileName))
    # 7.修改配置monitor.conf中的server类型
    remoteTools.run_cmd("cd {}/pstat_v1.0.4/conf && sed -i 's/server = {}/server = {}/' monitor.conf".format(
        start_path, init_server_kind, dst_server_kind))
    # 8.对启动脚本赋可执行权限
    remoteTools.run_cmd('chmod +x {}/start.sh'.format(start_path))
    # 9.执行start.sh脚本 (nohup your_shell.sh > /dev/null 2>&1 &)
    remoteTools.run_cmd('cd {} && sh start.sh'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 已执行完毕！！！'.format(ip))


def autoRestartMini2(ip, username, password, port, start_path):
    """
    远程重启流程
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.对启动脚本赋可执行权限
    remoteTools.run_cmd('chmod +x {}/start.sh'.format(start_path))
    # 4.执行start.sh脚本
    remoteTools.run_cmd('cd {} && sh start.sh'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 重启完毕！！！'.format(ip))


def autoStopMini2(ip, username, password, port):
    """
    远程停止流程
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.杀nmon进程
    remoteTools.run_cmd("ps -ef | grep nmon | grep -v grep | awk '{print $2}' | xargs kill -9")
    # 4.杀pstat进程
    remoteTools.run_cmd("ps -ef | grep pstat | grep -v grep | awk '{print $2}' | xargs kill -9")
    # 关闭连接
    remoteTools.close()
    print('ip = {} 资源监控已停止！！！'.format(ip))


def autoRemoveMini2(ip, username, password, port, remote_path):
    """
    远程删除监控脚本
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.杀nmon进程
    remoteTools.run_cmd("ps -ef | grep nmon | grep -v grep | awk '{print $2}' | xargs kill -9")
    # 4.杀pstat进程
    remoteTools.run_cmd("ps -ef | grep pstat | grep -v grep | awk '{print $2}' | xargs kill -9")
    # 5.删除脚本
    (path, fileName) = os.path.split(remote_path)
    file_dir = fileName.split('.')[0].strip()
    remoteTools.run_cmd("cd {} && rm -rf {}".format(path, file_dir))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 资源监控脚本已停止并删除！！！'.format(ip))


def autoStartGather(ip, username, password, port, local_path, remote_path, start_path, init_server_kind,
                    dst_server_kind, init_localhost):
    # 获取远端路径及文件名
    (remote_path1, fileName) = os.path.split(remote_path)
    print('ip={} remote_path ={} fileName={}\n上传中...'.format(ip, remote_path1, fileName))
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ftp连接
    remoteTools.ftpConnect()
    # 3.创建ssh连接
    remoteTools.connect()
    # 4.上传脚本文件
    remoteTools.upLoad(remote_path, local_path)
    # 5.tar -xf 解压
    remoteTools.run_cmd('cd {} && tar -xf {}'.format(remote_path1, fileName))
    # 6.删除压缩文件
    remoteTools.run_cmd('cd {} && rm -rf {}'.format(remote_path1, fileName))
    # 7.需要改gather配置文件中的hostname、localhost
    remoteTools.run_cmd(
        "cd {} && sed -i -e 's/hostname={}/hostname={}/' -e 's/localhost{}=/localhost={}/' gather".format(
            start_path, init_server_kind, dst_server_kind, init_localhost, ip))
    # 8.执行gather启动命令
    remoteTools.run_cmd('cd {} && sh gather restart'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 已执行完毕！！！'.format(ip))


def autoRestartGather(ip, username, password, port, start_path):
    """
    自动重启流程
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.执行gather重启命令
    remoteTools.run_cmd('cd {} && sh gather restart'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 重启完毕！！！'.format(ip))


def autoStopGather(ip, username, password, port, start_path):
    """
    远程停止流程
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.执行gather重启命令
    remoteTools.run_cmd('cd {} && sh gather stop'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 资源监控已停止！！！'.format(ip))


def autoRemoveGather(ip, username, password, port, start_path, remote_path):
    """
    远程删除监控脚本
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.执行gather重启命令
    remoteTools.run_cmd('cd {} && sh gather stop'.format(start_path))
    # 4.删除脚本
    (path, fileName) = os.path.split(remote_path)
    file_dir = fileName.split('.')[0].strip()
    remoteTools.run_cmd("cd {} && rm -rf {}".format(path, file_dir))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 资源监控脚本已停止并删除！！！'.format(ip))


def autoStartAmon(ip, username, password, port, local_path, remote_path, start_path):
    # 获取远端路径及文件名
    (remote_path1, fileName) = os.path.split(remote_path)
    print('ip={} remote_path ={} fileName={}\n上传中...'.format(ip, remote_path1, fileName))
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ftp连接
    remoteTools.ftpConnect()
    # 3.创建ssh连接
    remoteTools.connect()
    # 4.上传脚本文件
    remoteTools.upLoad(remote_path, local_path)
    # 5.执行脚本 unzip remote_path
    remoteTools.run_cmd('tar -xf {}'.format(remote_path))
    # 6.执行脚本 删除zip文件
    remoteTools.run_cmd('rm -rf {}'.format(remote_path))
    # 7.执行gather启动命令
    remoteTools.run_cmd('cd {} && sh start.sh'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 已执行完毕！！！'.format(ip))


def autoRestartAmon(ip, username, password, port, start_path):
    """
    自动重启流程
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.执行gather重启命令
    remoteTools.run_cmd('cd {} && sh stop.sh && sh start.sh'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 重启完毕！！！'.format(ip))


def autoStopAmon(ip, username, password, port, start_path):
    """
    远程停止流程
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.执行gather重启命令
    remoteTools.run_cmd('cd {} && sh stop.sh'.format(start_path))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 资源监控已停止！！！'.format(ip))


def autoRemoveAmon(ip, username, password, port, start_path, remote_path):
    """
    远程删除监控脚本
    """
    # 1.创建初始化RemoteServerTools
    remoteTools = RemoteServerTools(ip, username, password, port)
    # 2.创建ssh连接
    remoteTools.connect()
    # 3.执行gather重启命令
    remoteTools.run_cmd('cd {} && sh stop.sh'.format(start_path))
    # 4.删除脚本
    (path, fileName) = os.path.split(remote_path)
    file_dir = fileName.split('.')[0].strip()
    remoteTools.run_cmd("cd {} && rm -rf {}".format(path, file_dir))
    # 关闭连接
    remoteTools.close()
    print('ip = {} 资源监控脚本已停止并删除！！！'.format(ip))


if __name__ == "__main__":
    try:
        multiprocessing.freeze_support()
        # 创建异步进程池（非阻塞）
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        # 配置文件位置
        default_path = os.path.dirname(os.path.realpath(__file__))
        configFileName = default_path + '\server_info.csv'
        # 读取远程服务器信息
        csvTools = CsvTools(configFileName)
        serverDatas = csvTools.getCsvData()
        while True:
            choice = input("请输入序号 [1-远程部署监控；2-远程重启监控；3-远程停止监控；4-远程删除监控；0-退出] : ")
            if choice == '1':
                # 异步多进程处理
                for server in serverDatas:
                    if server['mon_type'] == 'miniconda2' or server['mon_type'] == 'pstat':
                        pool.apply(autoStartMini2, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['local_path'], server['remote_path'], server['start_path'],
                            'custom', server['server_kind']))
                    elif server['mon_type'] == 'gather':
                        pool.apply(autoStartGather, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['local_path'], server['remote_path'], server['start_path'],
                            'custom', server['server_kind'], 'localhost'))
                    elif server['mon_type'] == 'amon':
                        pool.apply(autoStartAmon, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['local_path'], server['remote_path'], server['start_path']))
                    else:
                        raise Exception(
                            f"报错信息 : \n输入的监控脚本类型为：{server['mon_type']}，目前仅支持miniconda2(pstat), gather, amon...")
            elif choice == '2':
                # 异步多进程处理
                for server in serverDatas:
                    if server['mon_type'] == 'miniconda2' or server['mon_type'] == 'pstat':
                        pool.apply(autoRestartMini2, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['start_path']))
                    elif server['mon_type'] == 'gather':
                        pool.apply(autoRestartGather, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['start_path']))
                    elif server['mon_type'] == 'amon':
                        pool.apply(autoRestartAmon, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['start_path']))
                    else:
                        raise Exception(
                            f"报错信息 : \n输入的监控脚本类型为：{server['mon_type']}，目前仅支持miniconda2(pstat), gather, amon...")
            elif choice == '3':
                # 异步多进程处理
                for server in serverDatas:
                    if server['mon_type'] == 'miniconda2' or server['mon_type'] == 'pstat':
                        pool.apply(autoStopMini2, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port'])))
                    elif server['mon_type'] == 'gather':
                        pool.apply(autoStopGather, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['start_path']))
                    elif server['mon_type'] == 'amon':
                        pool.apply(autoStopAmon, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['start_path']))
                    else:
                        raise Exception(
                            f"报错信息 : \n输入的监控脚本类型为：{server['mon_type']}，目前仅支持miniconda2(pstat), gather, amon...")
            elif choice == '4':
                # 异步多进程处理
                for server in serverDatas:
                    if server['mon_type'] == 'miniconda2' or server['mon_type'] == 'pstat':
                        pool.apply(autoRemoveMini2, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['remote_path']))
                    elif server['mon_type'] == 'gather':
                        pool.apply(autoRemoveGather, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['start_path'], server['remote_path']))
                    elif server['mon_type'] == 'amon':
                        pool.apply(autoRemoveAmon, args=(
                            server['ip'], server['username'], server['passwd'], int(server['port']),
                            server['start_path'], server['remote_path']))
                    else:
                        raise Exception(
                            f"报错信息 : \n输入的监控脚本类型为：{server['mon_type']}，目前仅支持miniconda2(pstat), gather, amon...")
            elif choice == '0':
                break
            else:
                print(f'输入的非法参数为：{choice}，请重新输入...')
        pool.close()
        pool.join()
    except Exception as e:
        print(f"报错信息 : \n{e}")
