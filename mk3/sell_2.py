import pandas as pd
import numpy as np
from pathlib import Path
from os import path
import sys

file_list = list(Path('./price_data').glob('*csv'))
file_name = path.basename(file_list[-1])

history = pd.read_csv('./histories.csv', encoding='sjis')

# mcadのデータ
mcad = pd.read_csv('mcad.csv', encoding='sjis')
# mcad

#historyデータにあるものだけ抽出
# list(history['SC'])
mcad = mcad[mcad['SC'].isin(list(history['SC']))]
# mcad

df_e = pd.DataFrame()
df_e['SC'] = mcad['SC']
df_e['名称'] = mcad['名称']
df_e['prev_signal'] = mcad.loc[:, mcad.columns[-10]:mcad.columns[-2]].mean(axis=1)
df_e['latest_signal'] = mcad.loc[:, mcad.columns[-9]:mcad.columns[-1]].mean(axis=1)
# df_e

# 計算間違っていたので追加
df_e['prev_kairi'] = mcad[mcad.columns[-2]] - df_e['prev_signal']
df_e['latest_kairi'] = mcad[mcad.columns[-1]] - df_e['latest_signal']

# df_e['diff'] = df_e['prev_signal'] - df_e['latest_signal']
df_e['diff'] = df_e['prev_kairi'] - df_e['latest_kairi']
df_e['flg'] = df_e['diff'].apply(lambda x: '1' if x > 0 else '0')
# df_e

new_data = pd.merge(history, df_e[['SC', 'flg']], on='SC', how='left')
new_data

## 売却値段を最新の株価とするため、最新データ取得
l_df = pd.read_csv('./price_data/' + file_name, encoding='sjis')
l_df = l_df[['SC', '株価']]
l_df.drop(l_df.index[0:2], inplace=True)
l_df = l_df[l_df['株価'] != '-']
l_df['株価'] = l_df['株価'].astype(str).astype(np.float64)
# l_df

new_data2 = pd.merge(new_data, l_df, on='SC', how='left')
# new_data2

new_data2.loc[new_data2['flg'] == '1', 'sell_price'] = new_data2['株価']

new_data2.loc[new_data2['flg'] == '1', 'sell_date'] = file_name[23:31]
# new_data2

# 売却が成立したものは、resultテーブルへ、そうでないものはそのまま
result_data = pd.read_csv('results.csv', encoding='sjis')
# result_data = pd.concat([result_data, history[history['sell_date'].isna() == False]])
result_data = pd.concat([result_data, new_data2[new_data2['sell_date'].isna() == False]])
history = new_data2[new_data2['sell_date'].isna() == True]

# historyから"flg", "株価"を削除
history = history[['SC', '名称', 'buy_date', 'buy_price', 'sell_date', 'sell_price']]

history.to_csv('./histories.csv', index=None, encoding='sjis')
result_data.to_csv('./results.csv', index=None, encoding='sjis')