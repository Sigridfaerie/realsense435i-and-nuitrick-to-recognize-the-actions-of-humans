# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/12/23 6:01 PM
# this file is used to provide some tools function
"""

import datetime
import time
import pyautogui
import os
import tkinter as tk
from tkinter import messagebox
def filename():
    "用于实时文件命名的函数"
    now = datetime.datetime.now()
    filename = now.strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    return filename

def show_message_box(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.attributes('-topmost', True)
    root.geometry("400x200")
def sleep_thread():
    while 1:
        # 等待按键事件
        #key = cv2.waitKey(1)
        print('start sleep')
        time.sleep(4)
        #print("Sleep Done")
        print("start store data")
        pyautogui.PAUSE = 1
        pyautogui.press('esc')
        print("esc 按下一次")

        # # 按下 ESC 键退出程序
        # if key == 27:
        #     break

def sleep_thread_one_time():
        print('===================开始采集动作=================================')
        time.sleep(6)
        #print("Sleep Done")
        print('====================start store data===========================')
       # pyautogui.PAUSE = 1
        pyautogui.press('esc')
        print("======================采集结束====================================")
def subdirectories(path):
    subdirectories = []
    for entry in os.scandir(path):
        if entry.is_dir():
            subdirectories.append(entry.name)
    return subdirectories
if __name__ == '__main__':

    sleep_thread()