注：

作用：windows实时资源监控展示；

该脚本需要调用的模块为：time, threading, tkiner, psutil

其中time, threading, tkiner模块均为python自带模块；

psutil模块，如本地尚未安装，则在cmd中python -m pip install pillow远程在线下载安装即可；

或离线安装pyWinMon文件夹下的"psutil-5.7.0-cp38-cp38-win_amd64.whl"文件

离线安装方式如下：

1，确保环境中已安装python

2，打开cmd后，cd /d 至pyWinMon文件夹下，输入：python -m pip install psutil-5.7.0-cp38-cp38-win_amd64.whl



使用说明：

在Windows下调用格式为：python pyWinMon.py

或双击pyWinMon\dist\pyWinMon.exe即可（该文件为打包后执行文件，无需python环境亦可运行）


