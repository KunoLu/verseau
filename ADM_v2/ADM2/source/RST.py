#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date      :  2020-12-05
@Author    :  KylinLu
@Email     :  lusonglin23@foxmail.com
@File      :  RST
@Software  :  PyCharm
"""
import paramiko


class RemoteServerTools:
    """
    远程工具类支持以下功能：
    1.上传文件
    2.下载文件
    3.远程执行命令
    """

    def __init__(self, remoteIp, username, password, remotePort=None):
        self.remoteIp = remoteIp
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.transport = None
        self.remotePort = remotePort
        self.sftp = None

    def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname=self.remoteIp, username=self.username, password=self.password)

    def ftpConnect(self):
        # 建立sftp连接
        self.transport = paramiko.Transport((self.remoteIp, self.remotePort))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def upLoad(self, remote_path, local_path):
        if self.sftp is None:
            print('请先建立sftp连接')
            return
        # 上传文件到远端服务器
        self.sftp.put(local_path, remote_path)
        print('ip={} 上传文件：{} 成功'.format(self.remoteIp, remote_path))

    def download(self, remote_path, local_path):
        if self.sftp is None:
            print('请先建立sftp连接')
            return
        # 下载远端服务器
        self.sftp.get(remote_path, local_path)
        print('ip = {} 下载文件：{} 成功'.format(self.remoteIp, local_path))

    def run_cmd(self, cmd):
        if self.client is None:
            print('请先建立ssh连接')
            return
        # 执行远端命令；get_pty开启伪终端，如果执行的命令为需持续运行的进程或服务改参数需为False
        stdin, stdout, stderr = self.client.exec_command(cmd, get_pty=True)
        # 获取命令结果
        result = stdout.read()
        channel = stdout.channel
        # 执行脚本结果
        status = channel.recv_exit_status()
        print('ip = {} 命令 = {} 执行结果={}'.format(self.remoteIp, cmd, status))
        if status != 0:
            print('ip = {} error = {}'.format(self.remoteIp, result))
        return status

    def close(self):
        # 关闭连接
        if self.client is not None:
            self.client.close()
        # 关闭远程连接
        if self.transport is not None:
            self.transport.close()
