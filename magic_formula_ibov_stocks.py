# coding=utf-8
"""This is script run the magic formula on ibov stocks."""

import warnings

import pandas as pd

warnings.filterwarnings("ignore")

url = "https://www.fundamentus.com.br/resultado.php"
df = pd.read_html(url, decimal=",", thousands=".")[0]

cs = ["Div.Yield", "Mrg Ebit", "Mrg. Líq.", "ROIC", "ROE", "Cresc. Rec.5a"]
for c in cs:
    df[c] = df[c].str.replace(".", "")
    df[c] = df[c].str.replace(",", ".")
    df[c] = df[c].str.rstrip("%").astype("float") / 100

df = df[df["Liq.2meses"] > 1000000]
df_than_zero = df[df["EV/EBIT"] > 0]

r = pd.DataFrame()
r["pos"] = range(1, 151)
r["EV/EBIT"] = df_than_zero.sort_values(by=["EV/EBIT"])["Papel"][:150].values
r["ROIC"] = df.sort_values(by=["ROIC"], ascending=False)["Papel"][:150].values

a = r.pivot_table(columns="EV/EBIT", values="pos")
b = r.pivot_table(columns="ROIC", values="pos")
t = pd.concat([a, b])
ranking = t.dropna(axis=1).sum()

print(ranking.sort_values()[:50])
