# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/12/23 6:01 PM
#
"""

import logging
import time

def log():
    """
    对日志信息进行处理，将其记录在文件中

    Returns:logger (logging.Logger): 日志记录器对象

    """
    # 创建一个名为mylog的logger对象
    logger = logging.getLogger('mylog')
    logger.setLevel(logging.DEBUG)

    # 创建一个输出到文件中的 handler 对象
    file_handler = logging.FileHandler('/home/polyuzed/Desktop/nuiproject/log/output.log')
    file_handler.setLevel(logging.DEBUG)

    # 创建一个 Formatter 对象，并设置格式化参数
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 将 handler 对象添加到 logger 对象中
    logger.addHandler(file_handler)
    return logger
# logger = log()
#
# # 在新线程和主线程中分别打印一些日志信息
# logger.info('This is the main thread')


