# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/12/23 8:52 PM
# This file is used for testing the model.
"""
# 此代码目的是测试训练的模型
from PyNuitrack import py_nuitrack
import cv2
import os
import numpy as np
from itertools import cycle
import csv
from ulits import filename
import tensorflow as tf
import threading
from ulits import sleep_thread_one_time
from loginfo import log
import pandas as pd
from databasic import generateds_onetime, stength_video

# label目录
mainpath = "dataset"
subdirectories = []
for entry in os.scandir(mainpath):
    if entry.is_dir():
        subdirectories.append(entry.name)
print(subdirectories)

# 定义绘制骨架的函数
def draw_skeleton(image):
    """
    绘制骨架并返回特定关节的投影数据

    Args:
        image (numpy.array): 图像数组

    Returns:
        datarow (list): 投影数据列表，包含10个关键点的位置信息
    """
    point_color = (59, 164, 0)

    # 遍历每个骨架中的关节,并循环写入数据
    for skel in data.skeletons:
        datarow = []
        for el in skel[1:]:
            # print(datarow)
            # datarow = el.
            x = (round(el.projection[0]), round(el.projection[1]))
            # 在图像上用圆形标识关节位置
            cv2.circle(image, x, 8, point_color, -1)
            dataitem = el.projection
            datarow.append(dataitem)
        datarow = [
            datarow[2], datarow[3], datarow[4], datarow[7], datarow[8],
            datarow[11], datarow[12], datarow[13], datarow[16], datarow[17]]
        # print(datarow)
        return datarow


# 初始化 Nuitrack 实例
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()

# 启动日志模块
logger = log()

# 创建新线程
t = threading.Thread(target=sleep_thread_one_time)
t.start()
logger.info('主线程启动开始')

# 创建骨架跟踪和深度图像模块
nuitrack.create_modules()
nuitrack.run()

datarows = []
# 定义循环显示模式的函数
modes = cycle(["depth","color"])
mode = next(modes)
while 1:
        # 等待按键事件
        key = cv2.waitKey(1)
        # 更新数据
        nuitrack.update()
        data = nuitrack.get_skeleton()
        img_depth = nuitrack.get_depth_data()
        if img_depth.size:
            # 将深度图像标准化到 0~255 范围内
            cv2.normalize(img_depth, img_depth, 0, 255, cv2.NORM_MINMAX)
            # 将深度图像转换为 RGB 图像
            img_depth = np.array(cv2.cvtColor(img_depth, cv2.COLOR_GRAY2RGB), dtype=np.uint8)
            img_color = nuitrack.get_color_data()
            # 在深度图像和彩色图像上绘制骨架
            datarow = draw_skeleton(img_depth)
            datarows.append(datarow)
            draw_skeleton(img_color)
            # 切换显示模式
            if key == 32:
                mode = next(modes)
            # 根据当前模式选择显示内容
            if mode == "depth":
                cv2.imshow('Image', img_depth)
            if mode == "color":
                if img_color.size:
                    cv2.imshow('Image', img_color)


        # 按下 ESC 键退出循环进入存储数据部分
        if key == 27:
            break

datarows = [datarow for datarow in datarows if datarow is not None]
#增加对于不足帧的补帧--暂时使用补足的方法
datarows = stength_video(datarows)

logger.info('存入测试动作数据')
column_names = [
        'left_collar',
        'left_elbow',
        'left_hand',
        'left_shoulder',
        'left_wrist',
        'right_collar',
        'right_elbow',
        'right_hand',
        'right_shoulder',
        'right_wrist']
path = "testapidata/"
filename = path + filename()
with open(filename, 'w', newline='') as file:
        # 创建csv writr 对象
        writer = csv.writer(file)
        # 写入列名
        writer.writerow(column_names)
        # 写入数据
        for datarow in datarows:
            writer.writerow(datarow)
        # print('写入文件的:', datarow)
logger.info('测试数据已经写入文件中')

# 释放资源
nuitrack.release()

#处理测试数据
# 设置CSV文件所在的文件夹路径
folder_path = filename
out_folder_path = filename
# 读取CSV文件
df = pd.read_csv(folder_path)
# 选择前100行（包括第一行作为列名）
df_selected = df.iloc[:100]
# 将结果覆盖原始文件
df_selected.to_csv(out_folder_path, index=False)

# Load data
data = generateds_onetime(out_folder_path)
X = np.array(data)
# Predict using the trained model
model = tf.keras.models.load_model("saved_model")
predictions = model.predict(X)
print(predictions)
# Print predictions
max_value = None
max_index = -1
for i, num in enumerate(predictions[0]):
    if max_value is None or num > max_value:
        max_index = i
        max_value = num
prediction = subdirectories[max_index]
print('The prediction is: %s'%prediction)
# if predictions[0][0] > predictions[0][1]:
#     print('The prediction is: wave')
# else:
#     print('The prediction is: applaud')



