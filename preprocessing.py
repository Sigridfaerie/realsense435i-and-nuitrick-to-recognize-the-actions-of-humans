# #_*_coding:utf-8_*_
"""
# @Author : Sigrid
# env python3.8
# @time   : 6/12/23 6:01 PM
# this file is used to process data csvs to standard their size
"""

import os
import pandas as pd

# 设置CSV文件所在的文件夹路径
folder_path = "data/action"
out_folder_path ="processeddata/test"

# 获取文件夹中的所有CSV文件路径
csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

# 遍历每个CSV文件，并取中间的100行数据
for file_path in csv_files:
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 取中间的100行
    num_rows = len(df)
    start_row = num_rows//2 - 50
    end_row = num_rows//2 + 50

    middle_rows = df.iloc[start_row:end_row, :]

    # 输出结果到新的CSV文件
    output_filename = os.path.basename(file_path).replace('.csv', '_middle_100_rows.csv')
    output_path = os.path.join(out_folder_path, output_filename)
    middle_rows.to_csv(output_path, index=False)
