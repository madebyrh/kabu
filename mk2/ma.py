from pathlib import Path
import pandas as pd
from os import path
import numpy as np
import sys

# 購入の判断は75日移動平均
moving_average = 25
price_data = []
file_list = list(Path('./price_data').glob('*.csv'))
# file_list = file_list[int(moving_average) * -1:]
file_list = file_list[(int(moving_average) + 1) * -1:]


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


def calc_mv(df, n=0, s=0):
    _total = 0
    for i in range(int(moving_average)):
        _total += df.iloc[n+i]
    return _total / int(moving_average)

## 移動平均記録用のデータフレームを作成する
mv_data = pd.DataFrame()
mv_data['SC'] = data['SC']
mv_data['名称'] = data['名称']

for i in range(2,data.shape[1]-int(moving_average) + 1):
    mv_data[str(data.columns[i + int(moving_average) - 1])] = data.apply(calc_mv, n=i, axis=1)
    
# mv_data

mv_data.to_csv('moving_average.csv', index=None, encoding='sjis')
    
                            