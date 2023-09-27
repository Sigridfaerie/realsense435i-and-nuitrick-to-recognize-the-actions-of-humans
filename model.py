# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/12/23 6:01 PM
"""
import tensorflow as tf

class CNN(tf.keras.Model):
    def __init__(self, num_classes):
        super(CNN, self).__init__()
        self.reshape = tf.keras.layers.Reshape((100, 30), input_shape=(100, 10, 3))
        self.conv1 = tf.keras.layers.Conv1D(64, 3, activation='relu')
        self.pool1 = tf.keras.layers.MaxPooling1D(2)
        self.conv2 = tf.keras.layers.Conv1D(128, 3, activation='relu')
        self.pool2 = tf.keras.layers.MaxPooling1D(2)
        self.conv3 = tf.keras.layers.Conv1D(256, 3, activation='relu')
        self.flat = tf.keras.layers.Flatten()
        self.dense1 = tf.keras.layers.Dense(256, activation='relu')
        self.dropout = tf.keras.layers.Dropout(0.5)
        self.dense2 = tf.keras.layers.Dense(num_classes, activation='softmax')

    def call(self, inputs):
        x = self.reshape(inputs)
        x = self.conv1(x)
        x = self.pool1(x)
        x = self.conv2(x)
        x = self.pool2(x)
        x = self.conv3(x)
        x = self.flat(x)
        x = self.dense1(x)
        x = self.dropout(x)
        x = self.dense2(x)
        return x
