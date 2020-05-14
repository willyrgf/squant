#!/usr/bin/env python3

import numpy as np
import pandas as pd
import string
import warnings
warnings.filterwarnings('ignore')

url = 'https://www.fundamentus.com.br/resultado.php'
df = pd.read_html(url, decimal=',', thousands='.')[0]

for coluna in ['Div.Yield', 'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Cresc. Rec.5a']:
  df[coluna] = df[coluna].str.replace('.', '')
  df[coluna] = df[coluna].str.replace(',', '.')
  df[coluna] = df[coluna].str.rstrip('%').astype('float') / 100

df = df[df['Liq.2meses'] > 1000000]

ranking = pd.DataFrame()
ranking['pos'] = range(1,151)
ranking['EV/EBIT'] = df[ df['EV/EBIT'] > 0 ].sort_values(by=['EV/EBIT'])['Papel'][:150].values
ranking['ROIC'] = df.sort_values(by=['ROIC'], ascending=False)['Papel'][:150].values

a = ranking.pivot_table(columns='EV/EBIT', values='pos')

b = ranking.pivot_table(columns='ROIC', values='pos')

t = pd.concat([a,b])

rank = t.dropna(axis=1).sum()

print(rank.sort_values()[:50])


