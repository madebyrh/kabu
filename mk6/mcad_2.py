import pandas as pd
import numpy as np
from os import path
from pathlib import Path

ema = pd.read_csv('ema.csv', encoding='sjis')
# ema

file_list = list(Path('./price_data').glob('*csv'))
file_name = path.basename(file_list[-1])
l_df = pd.read_csv('./price_data/' + file_name, encoding='sjis')
l_df = l_df[['SC', '株価']]
l_df.drop(l_df.index[0:2], inplace=True)
l_df = l_df[l_df['株価'] != '-']
l_df['株価'] = l_df['株価'].astype(str).astype(np.float64)
# l_df

new_data = pd.merge(ema, l_df, on='SC', how='left')
# new_data

# 平滑化定数を設定
alpha26 = 2 / (26 + 1)
alpha12 = 2 / (12 + 1)

new_data['ema26'] = new_data['ema26'] + alpha26 * (new_data['株価'] - new_data['ema26'])
new_data['ema12'] = new_data['ema12'] + alpha12 * (new_data['株価'] - new_data['ema12'])
# new_data

new_data.drop('株価', axis=1, inplace=True)
# new_data

new_data.to_csv('ema.csv', index=None, encoding='sjis')

filename_only = file_name[23:31]
# filename_only

mcad = pd.read_csv('mcad.csv', encoding='sjis')

mcad['SC'] = new_data['SC']
mcad['名称'] = new_data['名称']
mcad[filename_only] = new_data['ema12'] - new_data['ema26']

mcad.to_csv('mcad.csv', index=None, encoding='sjis')