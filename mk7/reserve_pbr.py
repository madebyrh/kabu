import pandas as pd
import numpy as np
from os import path
from pathlib import Path


df = pd.read_csv('./moving_average.csv', encoding='sjis')

file_list = list(Path('./price_data').glob('*csv'))
file_name = path.basename(file_list[-1])

l_df = pd.read_csv('./price_data/' + file_name, encoding='sjis')

l_df = l_df[['SC', '株価', '市場']]
l_df.drop(l_df.index[0:2], inplace=True)
l_df = l_df[l_df['市場'].isnull() == False]
l_df = l_df[l_df['株価'] != '-']
l_df['株価'] = l_df['株価'].astype(str).astype(np.float64)



# compare_data = pd.merge(df, l_df, on='SC', how='left')
compare_data = pd.merge(df, l_df, on='SC')
compare_data.drop(compare_data.columns[-1], axis=1,inplace=True)

compare_data['compare'] = compare_data[compare_data.columns[-2]] - compare_data[compare_data.columns[-1]]
# compare_data

tmp_data = compare_data.loc[compare_data['compare'] > .0]
tmp_data['rate'] = tmp_data['compare'] / tmp_data[tmp_data.columns[-3]]

# 結合した後のほうがいいか
tmp_data2 = tmp_data.sort_values(by='rate', ascending=True)[0:20]
# tmp_data2

# 移動平均が上昇傾向のもののみを対象にする
tmp_data2 = tmp_data2[tmp_data2[tmp_data2.columns[2]] < tmp_data2[tmp_data2.columns[3]]]

file_list = list(Path('./financial_data').glob('*csv'))
file_name = path.basename(file_list[-1])
# file_name

financial_data = pd.read_csv('./financial_data/' + file_name, encoding='sjis')
# financial_data

financial_data.drop(financial_data.index[0:2], inplace=True)
financial_data = financial_data[financial_data['PBR（実績）'] != '-']
financial_data['PBR（実績）'] = financial_data['PBR（実績）'].astype(str).astype(np.float64)

test_data = financial_data.copy()
test_data = test_data[['SC', 'PBR（実績）']]
tmp_data3 = pd.merge(tmp_data2, test_data, on='SC')
# tmp_data3


save_data = tmp_data3.sort_values(by='PBR（実績）', ascending=True)[0:5]



reserve_data = save_data.drop(save_data.columns[-1], axis=1)
#tmp_data3.columns[-1]
# reserve_data

reserve_data['reserve_price'] = (reserve_data[reserve_data.columns[2]] + 1.0).round()
# reserve_data

# 無理やりフォーマット
reserve_data.drop(reserve_data.columns[2], axis=1, inplace=True)

reserve_data.to_csv('reserve_data.csv', index=None, encoding='sjis')