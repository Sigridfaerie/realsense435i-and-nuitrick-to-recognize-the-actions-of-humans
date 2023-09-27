# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/12/23 6:01 PM
# this file is used to capture video datas continuously
"""

import time
import threading
from PyNuitrack import py_nuitrack
import cv2
import numpy as np
from itertools import cycle
import csv
from ulits import filename, sleep_thread
from loginfo import log


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
				#print(datarow)
				# datarow = el.
				x = (round(el.projection[0]), round(el.projection[1]))
				# 在图像上用圆形标识关节位置
				cv2.circle(image, x, 8, point_color, -1)
				dataitem = el.projection
				datarow.append(dataitem)
			datarow = [
				datarow[2], datarow[3], datarow[4], datarow[7],datarow[8],
				datarow[11], datarow[12], datarow[13], datarow[16],datarow[17]]
			#print(datarow)
			return datarow


# 初始化 Nuitrack 实例
nuitrack = py_nuitrack.Nuitrack()
nuitrack.init()


# 获取可用的 Nuitrack 设备列表
devices = nuitrack.get_device_list()
for i, dev in enumerate(devices):
	print(dev.get_name(), dev.get_serial_number())
	if i == 0:
		#dev.activate("ACTIVATION_KEY") #you can activate device using python api
		# 打印设备激活状态
		print(dev.get_activation())
		# 选择第一个设备并设置为当前使用设备
		nuitrack.set_device(dev)
#
# # 输出库版本和许可证信息
# print(nuitrack.get_version())
# print(nuitrack.get_license())

# 启动日志模块
logger = log()


# 创建新线程
t = threading.Thread(target=sleep_thread)
t.start()
logger.info('主线程启动开始')

# 创建骨架跟踪和深度图像模块
nuitrack.create_modules()
nuitrack.run()

while True:
	# # 创建新线程
	# t = threading.Thread(target=sleep_thread)
	# t.start()
	# 初始化数据集
	datarows = []
	# 定义循环显示模式的函数
	modes = cycle(["depth", "color"])
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
			img_depth = np.array(cv2.cvtColor(img_depth,cv2.COLOR_GRAY2RGB), dtype=np.uint8)
			img_color = nuitrack.get_color_data()
			# 在深度图像和彩色图像上绘制骨架
			datarow = draw_skeleton(img_depth)
			datarows.append(datarow)
			# print(datarows)
			draw_skeleton(img_color)
			# 面部追踪使用 否则注释
			# draw_face(img_depth)
			# draw_face(img_color)
			# 切换显示模式
			if key == 32:
				mode = next(modes)
			# 根据当前模式选择显示内容
			if mode == "depth":
				cv2.imshow('Image', img_depth)
			if mode == "color":
				if img_color.size:
					cv2.imshow('Image', img_color)
		# 按下 ESC 键退出程序
		if key == 27:
			break
		# # 按下 enter 键继续程序
		# if key == 16:
		# 	continue

	datarows = [datarow for datarow in datarows if datarow is not None]
	logger.info('总数据get')
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
	path = "data/action/"
	with open(path+filename(), 'w', newline='') as file:
		# 创建csv writr 对象
		writer = csv.writer(file)
		# 写入列名
		writer.writerow(column_names)
		# 写入数据
		for datarow in datarows:
			writer.writerow(datarow)
			#print('写入文件的:', datarow)
	logger.info('数据已经写入文件中')
# 释放资源
nuitrack.release()
