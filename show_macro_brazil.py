# coding=utf-8
"""This is script show brazil macro economics graphs."""

import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf

sns.set()

matplotlib.rcParams["figure.figsize"] = (16, 8)
matplotlib.rcParams.update({"figure.autolayout": True})
timestr = time.strftime("%Y%m%d_%H%M%S")


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

start_date = "2016-01-01"

ibov_diff_agg = (1 + ibov_diff[ibov_diff.index >= start_date]).cumprod()
ibov_diff_agg.iloc[0] = 1

cdi_agg = (1 + cdi[cdi.index >= start_date] / 100).cumprod()
cdi_agg.iloc[0] = 1
selic_meta_date = selic_meta[selic_meta.index >= start_date]
dollar_reserve_date = dollar_reserve[dollar_reserve.index >= start_date]
dollar_reserve_date_bi = dollar_reserve_date["valor"].div(1000000)

print(ibov_diff_agg)
print(cdi_agg)
print(selic_meta_date)
print(dollar_reserve_date_bi)

fig, ax = plt.subplots()
ax.set_title("show_macro_brazil.py")

ax.xaxis.set_label_text("Date")
ax.yaxis.set_label_text("Values")

ax.plot(ibov_diff_agg, label="ibov_return_agg")
ax.plot(cdi_agg, label="cdi_return_agg")
ax.plot(selic_meta_date, label="selic_meta")
ax.plot(dollar_reserve_date_bi, label="dollar_reserve_in_tri")

ax.legend(["ibov_return_agg", "cdi_return_agg", "selic_meta", "dollar_reserve_in_tri"])

fig.savefig("./downloads/show_macro_brazil_plot_" + timestr + ".png")
