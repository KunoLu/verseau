注：

该脚本需要调用的模块为：os, time, xlrd, matplotlib, imageio

其中os与time模块均为python自带模块；

其他模块在cmd中python -m pip install [模块名] 远程在线下载安装即可；

或离线安装dynamicDataFlowGraph/offlineLib文件夹下的whl后缀的离线安装包

离线安装方式如下：

1，确保环境中已安装python

2，打开cmd后，cd /d 至dynamicDataFlowGraph/offlineLib文件夹下，输入：python -m pip install [whl后缀的离线安装包]



使用说明：

1，修改 "data_source.xlsx"文件中的数据;

2，修改脚本，如使用"making_DDFG_standard.py"生成gif文件，data_gif(cols, xlim_num, duration)
#cols 展示前几列的数据，xlim_num x轴刻度值，duration 两张图片间的间隔，建议写0.2-0.5；

3，修改脚本，如使用"making_DDFG_advanced.py"生成gif文件，data_gif(cols, xlim_num, xlim_interval, duration,title_attach='')
# cols 展示前几列的数据，xlim_num x轴刻度值，duration 两张图片间的间隔，建议写0.2-0.5,title_attach 标题后附加部分，可不写

上述步骤修改完毕后，在Windows下调用格式为：
python making_DDFG_standard.py
or
python making_DDFG_advanced.py

