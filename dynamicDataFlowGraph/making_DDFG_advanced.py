"""
@author: KylinLu
@date: 20200215
"""

import xlrd
import matplotlib.pyplot as plt
import imageio
import os
import time

timeStamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
absPath = os.path.abspath('.')
pngPath = os.getcwd()
cPathDir = [x for x in os.listdir('.') if os.path.isdir(x)]
if 'gif' in cPathDir:
    print('gif dir exists...')
    pass
else:
    print('no gif dir...create gif dir')
    # 创建目录
    gifPath = os.path.join(absPath, 'gif')
    os.mkdir(gifPath)


def data_gif(cols, xlim_num, xlim_interval, duration,
             title_attach=''):  # cols 展示前几列的数据，xlim_num x轴刻度值，duration 两张图片间的间隔，建议写0.2-0.5,title_attach 标题后附加部分，可不写

    frames = []
    xlsx = xlrd.open_workbook('data_source.xlsx')
    sheet = xlsx.sheet_by_index(0)
    name_list = []
    for j in range(1, int(cols)):
        name_list.append(sheet.cell_value(0, j))

    for i in range(1, sheet.nrows):
        row_data_list = []
        for j in range(1, int(cols)):
            title = sheet.cell_value(i, 0)
            row_data = sheet.cell_value(i, j)
            row_data_list.append(float(row_data))
        font = {'family': 'SimHei',
                'style': 'normal',
                'weight': 'normal',
                'color': '#FFFFFF',
                'size': 20,

                }
        plt.rcParams['figure.figsize'] = (16.0, 9.0)

        plt.rcParams['axes.facecolor'] = '#0D0434'
        plt.rcParams['savefig.facecolor'] = '#0D0434'
        plt.rcParams['xtick.color'] = '#FFFFFF'
        plt.rcParams['ytick.color'] = '#FFFFFF'
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.tick_params(labelsize=20)
        plt.xlim((0, int(xlim_num)))
        plt.xticks(range(0, xlim_num, xlim_interval))
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.xaxis.label.set_color('red')
        # ax.tick_params(axis='x', colors='red')
        # ax.yaxis.label.set_color('red')
        # ax.tick_params(axis='y', colors='red')

        m = 0

        for n in row_data_list:
            plt.text(int(xlim_num) / 10, m, str(n), ha='left', va='center', fontdict=font)
            m += 1
        plt.barh(name_list, row_data_list, height=0.35, facecolor='#2C43C2', edgecolor='white')
        plt.title(str(title) + str(title_attach), fontdict=font)
        plt.savefig('%s.png' % str(title))
        plt.close('all')

        im = imageio.imread('%s.png' % str(title))
        frames.append(im)
    imageio.mimsave(r'gif\gif_%s.gif' % timeStamp, frames, 'GIF', duration=round(duration, 2))


def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))


if __name__ == "__main__":
    data_gif(7, 800, 200, 0.5, '价格指数')
    del_files(pngPath)
