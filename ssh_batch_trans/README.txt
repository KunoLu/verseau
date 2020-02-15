注：

该脚本需要调用的模块为：paramiko, sys, datetime, threading, queue, getopt

其中sys, datetime, threading, queue, getopt模块均为python自带模块；

paramiko模块在cmd中python -m pip install paramiko远程在线下载安装即可；

或离线安装ssh_batch_trans/offlineLib文件夹下的whl后缀的离线安装包

离线安装方式如下：

1，确保环境中已安装python

2，打开cmd后，cd /d 至ssh_batch_trans/offlineLib文件夹下，输入：python -m pip install [whl后缀的离线安装包]



使用说明：

在Windows下调用格式为：

python timingScreenshots.py 	# 显示帮助文档，详细操作指南见帮助文档内容

          -h,-H,--help         帮助页面 
              -C, --cmd            执行命令模式 
              -M, --command        执行具体命令 
              -S, --sendfile       传输文件模式 
              -L, --localpath      本地文件路径 
              -R, --remotepath     远程服务器路径 
	    IP列表格式:
   	    IP地址		   用户名  密码     端口
	    192.168.1.1    root	  123456   22
      	e.g.
            批量执行命令格式： -C "IP列表" -M '执行的命令'
            批量传送文件：     -S "IP列表" -L "本地文件路径" -R "远程文件路径"
	    错误日志文件：$PWD/ssh_errors.log


