import pandas as pd
import numpy as np
from os import path
from pathlib import Path
import sys


# moving_average = sys.argv[1]

df = pd.read_csv('./moving_average.csv', encoding='sjis')

# file_list = list(Path('./latest_data').glob('*.csv'))
# file_name = path.basename(file_list[-1])

file_list = list(Path('./price_data').glob('*csv'))
file_name = path.basename(file_list[-1])

# l_df = pd.read_csv('./latest_data/' + file_name, encoding='sjis')
l_df = pd.read_csv('./price_data/' + file_name, encoding='sjis')
l_df = l_df[['SC', '株価']]
l_df.drop(l_df.index[0:2], inplace=True)
l_df = l_df[l_df['株価'] != '-']
l_df['株価'] = l_df['株価'].astype(str).astype(np.float64)
l_df

compare_data = pd.merge(df, l_df, on='SC', how='left')
# compare_data

tmp = compare_data[compare_data.columns[-2]] - compare_data[compare_data.columns[-1]]
compare_data['compare'] = tmp
# compare_data

# 移動平均 > 株価 のデータのみ抽出
tmp_data = compare_data.loc[compare_data['compare'] > .0]
# tmp_data

# 割合(移動平均線への近づき具合)wを求める
tmp_data['rate'] = tmp_data['compare'] / tmp_data[tmp_data.columns[-3]]
# tmp_data

# rateの値が小さい順にsortする
tmp_data.sort_values(by='rate', ascending=True)

save_data = tmp_data.sort_values(by='rate', ascending=True)[0:10]

reserve_data = save_data.drop(save_data.columns[2:-4], axis=1)

## 購入予定価格の設定
import math
def ceiling(df):
    return math.ceil(df[df.columns[2]] + 1.0)
reserve_data['reserve_price'] = (reserve_data[reserve_data.columns[2]] + 1.0).round()
#reserve_data['reserve_price'] = reserve_data.apply(ceiling)

reserve_data.to_csv('reserve_data.csv', index=None, encoding='sjis')