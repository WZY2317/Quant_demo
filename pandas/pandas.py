import pandas as pd
import numpy as np

data = pd.read_csv(
    'C:\Users\26856\Documents\GitHub\Quant_demo\pandas\000001.csv',
    dtype=object)
data.head(10)
# arr = np.array([1, 'hhh', 3, 4], dtype=object)
# print(arr)
# print(arr.dtype)
