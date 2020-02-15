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
	

def data_gif(cols, xlim_num, duration):#cols 展示前几列的数据，xlim_num x轴刻度值，duration 两张图片间的间隔，建议写0.2-0.5
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
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
        plt.xlim((0, int(xlim_num)))
        plt.barh(name_list, row_data_list, color='blue')
        plt.savefig("%s.png" % str(title))
        plt.close('all')
		
        im = imageio.imread("%s.png" % str(title))
        frames.append(im)
    imageio.mimsave(r'gif\gif_%s.gif' % timeStamp, frames, 'GIF', duration=round(duration, 2))


def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))


if __name__ == "__main__":
	data_gif(7,1000,0.5)
	del_files(pngPath)
