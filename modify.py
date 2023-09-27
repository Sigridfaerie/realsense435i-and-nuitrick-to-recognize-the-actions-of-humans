# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/14/23 6:34 PM
"""
import pandas as pd
import numpy as np

x = [np.zeros(3) for i in range(10)]


datarows =np.ones((10, 3))
while len(datarows) < 10:
    diff = 10 - len(datarows)
    new_array = np.zeros((10, 3))
    datarows.append(new_array)
print(datarows)
print(len(datarows))