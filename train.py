# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/13/23 2:03 PM
# this file is used to train model and save model
"""

import os
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from model import CNN
import tensorflow as tf
from databasic import generateds, normalize_data
from ulits import subdirectories
# Load data
X = []
Y = []
# 获取当前脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 数据集在当前脚本目录下的子目录中
#path = os.path.join(script_dir, "dataset")

path = "dataset"
X, Y = generateds(path)
X = np.array(X)
Y = np.array(Y)
# Split data into training, validation and testing sets
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.1, random_state=42)

# 打印数据形状
print("X_train shape:", x_train.shape)
print("y_train shape:", len(y_train))
print("X_test shape:", x_test.shape)
print("y_test shape:", len(y_test))

#归一化
x_train = normalize_data(x_train)
x_val = normalize_data(x_val)
x_test = normalize_data(x_test)

#reshape 成 张量
x_train = tf.convert_to_tensor(x_train)
x_val = tf.convert_to_tensor(x_val)
x_test = tf.convert_to_tensor(x_test)

# classes
num_classes = len(subdirectories(path))

# 将训练集、验证集和测试集的字符串标签映射为整数标签
label_mapping = {label: i for i, label in enumerate(subdirectories(path))}
y_train = np.array([label_mapping[label] for label in y_train])
y_val = np.array([label_mapping[label] for label in y_val])
y_test = np.array([label_mapping[label] for label in y_test])

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
y_val = tf.keras.utils.to_categorical(y_val, num_classes=num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=num_classes)

# Create model
model = CNN(num_classes=num_classes)

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train model
model.fit(x_train, y_train,
          batch_size=32,
          epochs=10,
          validation_data=(x_val, y_val))

# save model
model.save('saved_model')

# Evaluate model
loss, acc = model.evaluate(x_test, y_test)
print('Test accuracy:', acc)
