import pandas as pd
import numpy as np
from os import path
from pathlib import Path

price_data = []
file_list = list(Path('./price_data').glob('*.csv'))
# file_12ma = file_list[-12:]
# 26ファイル取得
file_list = file_list[-26:]
#print(len(file_12ma))
#print(len(file_26ma))

base_filename = path.splitext(path.basename(file_list[0]))[0][23:]
data = pd.read_csv(file_list[0], encoding='sjis')
data = data[['SC', '名称', '株価']]
data.drop(data.index[0:2], inplace=True)
# 欠損値の削除
data = data[data['株価'] != '-']
# 数値に変換
data['株価'] = data['株価'].astype(str).astype(np.float64)
data.rename(columns={'株価': base_filename}, inplace=True)
#data[base_filename] = data[base_filename].astype(str).astype(np.float64)
data = data.set_index('SC')

tmp_list = []
for index, elm in enumerate(file_list):
    if index == 0:
        continue
    filename = path.splitext(path.basename(elm))[0][23:]
    tmp_data = pd.read_csv(elm, encoding='sjis')
    tmp_data = tmp_data[['SC', '株価']]
    # 欠損値の削除
    tmp_data = tmp_data[tmp_data['株価'] != '-']
    # 数値に変換
    tmp_data['株価'] = tmp_data['株価'].astype(str).astype(np.float64)
    tmp_data.rename(columns={"株価": filename}, inplace=True)
    tmp_data.drop(tmp_data.index[0:2], inplace=True)
    
    tmp_data = tmp_data.set_index('SC')
    tmp_list.append(tmp_data)
data = data.join(tmp_list)
data.reset_index(inplace=True)
# data.head()

data.loc[:,data.columns[-26]:data.columns[-1]]

data['ema26'] = data.loc[:,data.columns[-26]:data.columns[-1]].mean(axis=1)
data['ema12'] = data.loc[:,data.columns[-12]:data.columns[-1]].mean(axis=1)
# data

data = data[['SC', '名称', 'ema26', 'ema12']]

data.to_csv('ema.csv', index=None, encoding='sjis')