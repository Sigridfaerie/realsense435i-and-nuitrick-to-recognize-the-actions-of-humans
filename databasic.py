# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/12/23 10:05 PM
# This file is used for pre-processing input data for the model.
"""

import os
import pandas as pd
import numpy as np
import csv

# 获取当前脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 数据集在当前脚本目录下的子目录中
mainpath = os.path.join(script_dir, "dataset")
def generateds(path):
    """
    处理训练数据用

    Args:
        path (str): 数据集所在路径

    Returns:
        X (list): 数据列表，由多个二维数组组成，每个二维数组代表一个数据样本
        Y (list): 标签列表，每个元素代表一个数据样本的标签，每个标签为'wave'或'applaud'之一
    """
    Y = [] #label
    X = [] #data
    subdirectories = []
    # data = None
    for entry in os.scandir(mainpath):
        if entry.is_dir():
            subdirectories.append(entry.name)
    print(subdirectories)
    for label in subdirectories:
    # for label in ['applaud', 'wave', 'towards_left', 'towards_right']:
        for filename in os.listdir(os.path.join(path, label)):
            if not filename.endswith('.csv'):
                continue
            Y.append(label)
            data = None
            with open(os.path.join(path, label, filename), 'r') as file:
                reader = csv.reader(file)
                next(reader) # Skip the header row
                file_data = []
                for row in reader:
                    row_data = []
                    for item in row:
                        item = item.strip()  # remove leading/trailing white space
                        if item.startswith('[') and item.endswith(']'):
                            item = item[1:-1]  # remove the brackets
                            subitems = item.split()
                            subitems = [float(subitem) for subitem in subitems]
                            row_data.append(subitems)
                        else:
                            row_data.append(float(item))
                    file_data.append(row_data)
            if data is None:
                data = np.array(file_data)
            else:
                data = np.concatenate((data, file_data), axis=0)
            X.append(data)
            # data = None
    return X, Y

#处理接口测试数据用
def generateds_onetime(path):
    """
    读取单个csv文件

    Args:
        path (str): 数据文件所在路径

    Returns:
        X (list): 数据列表，由一个二维数组组成，代表一个数据样本
    """
    X = [] #data
    data = None
    with open(os.path.join(path), 'r') as file:
                reader = csv.reader(file)
                next(reader) # Skip the header row
                file_data = []
                for row in reader:
                    row_data = []
                    for item in row:
                        item = item.strip()  # remove leading/trailing white space
                        if item.startswith('[') and item.endswith(']'):
                            item = item[1:-1]  # remove the brackets
                            subitems = item.split()
                            subitems = [float(subitem) for subitem in subitems]
                            row_data.append(subitems)
                        else:
                            row_data.append(float(item))
                    file_data.append(row_data)
    if data is None:
        data = np.array(file_data)
    else:
        data = np.concatenate((data, file_data), axis=0)
    X.append(data)
    return X


def normalize_data(data):
    """
    对数据进行归一化-->cnn需求

    Args:
        data (numpy.array): 输入数据，二维数组形式

    Returns:
        data_normalized (numpy.array): 归一化后的数据，二维数组形式
    """
    numeric_data = np.zeros_like(data, dtype=float)
    for i in range(len(data)):
        for j in range(len(data[i])):
            a = data[i][j]
            b = numeric_data[i][j]
            if isinstance(data[i][j], str):
                numeric_data[i][j] = float(data[i][j])
            else:
                numeric_data[i][j] = data[i][j]
    min_vals = np.min(numeric_data, axis=0)
    max_vals = np.max(numeric_data, axis=0)
    data_normalized = (numeric_data - min_vals) / (max_vals - min_vals)
    return data_normalized

#修改时间过短动作导致视频无法采集沟100帧问题
def stength_video(videoarray):
    """
    对视频数据进行处理，使其长度达到100

    Args:
        videoarray (list): 输入视频数据，由多个含有三个元素的数组组成

    Returns:
        videoarray_new (list): 处理后的视频数据，长度为100，由多个含有三个元素的数组组成
    """
    added = [np.zeros(3) for i in range(10)]
    while len(videoarray) < 100:
        #diff = 100 - len(videoarray)
        videoarray.append(added)
    return videoarray





#path = "dataset/"
path = os.path.join(script_dir, "dataset")
#data = generateds_onetime('dataset/wave/2023-06-12-18-13-13_middle_100_rows.csv')
data = generateds(mainpath)
print(data)
#data =
# x_train, y_train = generateds(path)
# print(y_train)