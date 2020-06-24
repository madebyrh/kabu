import pandas as pd
import numpy as np
from os import path
from pathlib import Path

# cat = '東証二部'

df = pd.read_csv('./moving_average.csv', encoding='sjis')

file_list = list(Path('./price_data').glob('*csv'))
file_name = path.basename(file_list[-1])
# file_name

l_df = pd.read_csv('./price_data/' + file_name, encoding='sjis')

# 変更
l_df = l_df[['SC', '株価', '市場']]
l_df.drop(l_df.index[0:2], inplace=True)
# l_df = l_df[l_df['市場'] == cat]
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

# tmp_data2 = tmp_data.sort_values(by='rate', ascending=True)[0:30]
# tmp_data2 = tmp_data2[tmp_data2[tmp_data2.columns[2]] < tmp_data2[tmp_data2.columns[3]]]
tmp_data2 = tmp_data.sort_values(by='rate', ascending=True)[0:100]
# tmp_data2
tmp_data2 = tmp_data2.sort_values(by='compare', ascending=False)[0:30]
# 移動平均が上昇傾向のもののみを対象にする
tmp_data2 = tmp_data2[tmp_data2[tmp_data2.columns[2]] < tmp_data2[tmp_data2.columns[3]]]

file_list = list(Path('./financial_data').glob('*csv'))
file_name = path.basename(file_list[-1])
# file_name

financial_data = pd.read_csv('./financial_data/' + file_name, encoding='sjis')
# financial_data

financial_data.drop(financial_data.index[0:2], inplace=True)
financial_data = financial_data[financial_data['PER（予想）'] != '-']
financial_data['PER（予想）'] = financial_data['PER（予想）'].astype(str).astype(np.float64)

# PBR追加
financial_data = financial_data[financial_data['PBR（実績）'] != '-']
financial_data['PBR（実績）'] = financial_data['PBR（実績）'].astype(str).astype(np.float64)
financial_data = financial_data[financial_data['配当利回り'] != '-']
financial_data['配当利回り'] = financial_data['配当利回り'].astype(str).astype(np.float64)

gyosyu_list = list(financial_data['業種'].unique())

class cat:
    def __init__(self, ave, std):
        self.ave = ave
        self.std = std

dictio = {}
for elm in gyosyu_list:
    # 平均
    #rint(financial_data[financial_data['業種'] == elm]['PER（予想）'].mean()
    #rint(financial_data[financial_data['業種'] == elm]['PER（予想）'].std())
    mean = financial_data[financial_data['業種'] == elm]['PER（予想）'].mean()
    std = financial_data[financial_data['業種'] == elm]['PER（予想）'].std()
    dictio[elm] = cat(mean, std)

financial_data['業種'] = financial_data['業種'].astype(str)

mean_list = []
std_list = []
for elm in list(dictio.keys()):
    mean_list.append(dictio[elm].ave)
    std_list.append(dictio[elm].std)
    

new_dic = {}
new_dic['業種'] = list(dictio.keys())
new_dic['平均'] = mean_list
new_dic['標準偏差'] = std_list
df = pd.DataFrame.from_dict(new_dic)
df['業種'] = df['業種'].astype(str)
# df.dtypes

test_data = pd.merge(financial_data, df, on='業種', how='left')

test_data['PER'] = (test_data['PER（予想）'] - test_data['平均']) / test_data['標準偏差']
# test_data

tmp_data3 = pd.merge(tmp_data2, test_data, on='SC')
# tmp_data3

save_data = tmp_data3.sort_values(by='PER', ascending=True)[0:7]
# save_data

save_data2 = save_data.copy()
save_data2 = save_data.sort_values(by='PBR（実績）', ascending=True)[0:5]
# save_data2

save_data3 = save_data2.copy()
save_data3 = save_data2.sort_values(by='配当利回り', ascending=False)[0:3]
# save_data3

reserve_data = save_data3.iloc[:, 0: -3]

reserve_data['reserve_price'] = (reserve_data[reserve_data.columns[2]] + 1.0).round()
# reserve_data

# 無理やりフォーマット
reserve_data.drop(reserve_data.columns[2], axis=1, inplace=True)

reserve_data.to_csv('reserve_data.csv', index=None, encoding='sjis')