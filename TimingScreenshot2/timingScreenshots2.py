#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-02-21
@Author: KylinLu
@Email: lusonglin23@foxmail.com
@Software: PyCharm
@File: timingScreenshots2.py
"""
import os
import time
import threading
from tkinter import *
from PIL import ImageGrab


# 倒计时截屏
def countDown_ss():
    status = '启动计时截屏！等待中...'
    t2.set(status)
    while float(e.get()):
        time.sleep(0.1)
        v = str(round(float(e.get()) - 0.1, 1))
        e['text'] = v
        e.delete(0, END)
        e.insert(0, v)
        e.update()
        if e['text'] == '0.0':
            nowtime = time.strftime('%Y%m%d_%H%M%S', time.localtime())
            # print(nowtime)
            im = ImageGrab.grab()  # 截屏
            im.save(r'png\%s.png' % (nowtime))  # 保存
            status = '截屏完毕！'
            t2.set(status)
            break


# 获取当前时间戳
def get_time():
    while True:
        c_time = time.strftime('%Y{y}%m{m}%d{d} %H:%M:%S', time.localtime()).format(y='年', m='月', d='日')
        t1.set(c_time)
        time.sleep(1)


if __name__ == '__main__':
    # 这里是为了如果找不到png这个目录的情况自己建一个png目录
    absPath = os.path.abspath('.')
    path = [x for x in os.listdir('.') if os.path.isdir(x)]
    # print(path)
    if 'png' in path:
        # print('png dir exists...')
        pass
    else:
        # print('no png dir...create png dir')
        # 创建目录
        pngPath = os.path.join(absPath, 'png')
        os.mkdir(pngPath)

    master = Tk()
    t1 = StringVar()
    t2 = StringVar()
    master.title("定时截屏")  # 窗口标题
    master.geometry("350x80+100+100")  # 窗口呈现大小和位置
    Label(master, text='延迟截屏时间(单位：秒)：').grid(row=0, column=0)
    e = Entry(text='0')
    e.grid(row=0, column=1)
    Button(master, text='倒计时', command=countDown_ss, fg='red').grid(row=0, column=2)
    Label(master, text='当前时间：').grid(row=1, column=0)
    Label(master, textvariable=t1).grid(row=1, column=1, columnspan=2)
    Label(master, text='截屏状态：').grid(row=2, column=0)
    Label(master, textvariable=t2).grid(row=2, column=1, columnspan=2)
    status = '尚未截屏！'
    t2.set(status)
    th1 = threading.Thread(target=get_time)
    th1.setDaemon(True)  # 守护线程
    th1.start()
    master.mainloop()

