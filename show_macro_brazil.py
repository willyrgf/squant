#!/usr/bin/env python3

import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import yfinance as yf

import matplotlib

matplotlib.rcParams['figure.figsize'] = (16,8)

"""# Obtendo Dados através da API do Banco Central do Brasil"""

def consulta_bc(codigo_bcb):
  url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
  df = pd.read_json(url)
  df['data'] = pd.to_datetime(df['data'], dayfirst=True)
  df.set_index('data', inplace=True)
  return df

"""# Exemplo de Consultas à API do Banco Central do Brasil"""

ipca = consulta_bc(433)

igpm = consulta_bc(189)

selic_meta = consulta_bc(432)
selic_meta.plot()

reservas_internacionais = consulta_bc(13621)

reservas_internacionais.plot()

pnad = consulta_bc(24369)
pnad



"""# CDI vs IBOV"""

ibov = yf.download(tickers='^BVSP')[['Adj Close']]

ibov_retorno = ibov.pct_change()

cdi = consulta_bc(12)

data_inicio = '2000-01-01'

ibov_retorno_acumulado = (1 + ibov_retorno[ibov_retorno.index >= data_inicio]).cumprod()
ibov_retorno_acumulado.iloc[0] = 1

cdi_acumulado = (1 + cdi[cdi.index >= data_inicio] / 100).cumprod()
cdi_acumulado.iloc[0] = 1

fig, ax = plt.subplots()
plt.plot(ibov_retorno_acumulado)
plt.plot(cdi_acumulado)

