# coding=utf-8
"""This is script show brazil macro economics graphs."""

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf

sns.set()

matplotlib.rcParams["figure.figsize"] = (16, 8)


def get_bc_data(cod_bc):
    """Get the data from Brazilian Central Bank."""
    burl = "http://api.bcb.gov.br"
    url = burl + "/dados/serie/bcdata.sgs.{}/dados?formato=json".format(cod_bc)
    df = pd.read_json(url)
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)
    df.set_index("data", inplace=True)
    return df


ipca = get_bc_data(433)
igpm = get_bc_data(189)
selic_meta = get_bc_data(432)
selic_meta.plot()

dollar_reserve = get_bc_data(13621)
dollar_reserve.plot()

pnad = get_bc_data(24369)
pnad

ibov = yf.download(tickers="^BVSP")[["Adj Close"]]
ibov_diff = ibov.pct_change()

cdi = get_bc_data(12)

start_date = "2000-01-01"

ibov_diff_agg = (1 + ibov_diff[ibov_diff.index >= start_date]).cumprod()
ibov_diff_agg.iloc[0] = 1

cdi_agg = (1 + cdi[cdi.index >= start_date] / 100).cumprod()
cdi_agg.iloc[0] = 1

fig, ax = plt.subplots()
plt.plot(ibov_diff_agg)
plt.plot(cdi_agg)
