注：

该脚本需要调用的模块为：os, time, PIL

其中os与time模块均为python自带模块；

PIL模块在python3之后即为pillow模块，如本地尚未安装，则在cmd中python -m pip install pillow远程在线下载安装即可；

或离线安装TimingScreenshots文件夹下的"Pillow-7.0.0-cp38-cp38-win_amd64.whl"文件

离线安装方式如下：

1，确保环境中已安装python

2，打开cmd后，cd /d 至TimingScreenshots文件夹下，输入：python -m pip install Pillow-7.0.0-cp38-cp38-win_amd64.whl



使用说明：

修改 "timingScreenshots.py"脚本中的s变量即可，s变量即为延迟截图的秒数。

在Windows下调用格式为：python timingScreenshots.py


