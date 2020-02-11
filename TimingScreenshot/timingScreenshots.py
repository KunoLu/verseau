"""
@author: KylinLu
@date: 20200210
"""

import time
from PIL import ImageGrab
import os

s = 10

# 这里是为了如果找不到png这个目录的情况自己建一个png目录
absPath = os.path.abspath('.')
path = [x for x in os.listdir('.') if os.path.isdir(x)]
# print(path)
if 'png' in path:
    print('png dir exists...')
    pass
else:
    print('no png dir...create png dir')
    # 创建目录
    pngPath = os.path.join(absPath, 'png')
    os.mkdir(pngPath)


# 截屏
def Screenshot():
    nowtime = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    print(nowtime)
    # 截屏语句很简单的
    im = ImageGrab.grab()
    # 保存（图里有png路径或者别的路径需要在这个路径下有这个目录，不然报错，所以我前面是做了规避，没路径我就自己建一个）
    im.save(r'png\%s.png' % (nowtime))


# while True:
#     print("Screenshot!")
#     Screenshot()
#     print("Pause...")
#     print("\n")
#     time.sleep(s)  # 定时10s看一下

screenshot_time = time.strftime('%Y{y}%m{m}%d{d} %H%M%S', time.localtime()).format(y='年', m='月', d='日')
print("Prepare the screenshot from : %s" % screenshot_time)
print("Screenshot in %s seconds..." % s)
time.sleep(s)
Screenshot()
print("Screenshot completed!")
