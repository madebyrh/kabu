import pandas as pd
import numpy as np
from pathlib import Path
from os import path
import sys
import datetime

# moving_average = sys.argv[1]

#file_list = list(Path('./latest_data').glob('*csv'))
#file_list[0]
#file_name = path.splitext(path.basename(file_list[0]))[0]
#file_name[23:]

file_list = list(Path('./price_data').glob('*csv'))
file_name = path.basename(file_list[-1])

# latest_data = pd.read_csv('./latest_data/' + file_name + '.csv', encoding='sjis')
latest_data = pd.read_csv('./price_data/' + file_name, encoding='sjis')

reserve_data = pd.read_csv('reserve_data.csv', encoding='sjis')

tmp_data = latest_data[latest_data['SC'].isin(list(reserve_data['SC']))]



tmp_data2 = pd.merge(tmp_data[['SC', '名称','株価']], reserve_data[['SC', 'reserve_price']], on=['SC'], how='left')
tmp_data2 = tmp_data2[tmp_data2['株価'] != '-']
tmp_data2['株価'] = tmp_data2['株価'].astype(str).astype(np.float64)

tmp_data3 = tmp_data2.copy()

#tmp_data3.drop(tmp_data3['株価'] == tmp_data3['reserve_price'], inplace=True, axis=1)
#tmp_data3.drop(tmp_data3[tmp_data3.columns[2]] > .1, inplace=True)
tmp_data3 = tmp_data3[tmp_data2['株価'] > tmp_data2['reserve_price']]
# tmp_data3['buy_date'] = file_name[23:]
tmp_data3['buy_date'] = file_name[23:31]
#tmp_data3['buy_date'] = datetime.date.today()

tmp_data2['株価'] > tmp_data2['reserve_price']

history = pd.read_csv('./histories.csv', encoding='sjis')

## historyテーブルに登録するために、フォーマットをあわせる
tmp_data3.drop('株価', axis=1, inplace=True)
tmp_data3.rename(columns={'reserve_price': 'buy_price'}, inplace=True)

# 結合する
concat_data = pd.concat([history, tmp_data3], axis=0)

concat_data.to_csv('./histories.csv', encoding='sjis', index=None)