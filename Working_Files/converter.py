# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import yfinance as yf
import panel as pn
import os
import ipywidgets as widgets
import requests
from requests import api
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI


# %%
pn.extension("plotly")
import plotly.express as px


# %%
#Country Codes
country_currency = api.get('http://country.io/currency.json').json()

# countries2 = api.get('https://restcountries.eu/rest/v2/').json()
# countries2


# %%
df_country_currency = pd.DataFrame(columns=['Code', 'Curr_code'], dtype=object)
for key,value in country_currency.items():
    df_country_currency = df_country_currency.append(pd.Series(
    [
        key,
        value
    ], index= df_country_currency.columns ), ignore_index=True)


# %%
df_country_currency.set_index('Code',inplace=True)
df_country_currency.head()


# %%
#Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=AUD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=AUD"

btc_url = btc_url + "?format=json"
eth_url = eth_url + "?format=json"

# %% [markdown]
# # Gathering Crypto Data

# %%
# Fetch current BTC price
btc_price = requests.get(btc_url)

# Fetch current ETH price
eth_price = requests.get(eth_url)

btc_response = btc_price.content
eth_response = eth_price.content

btc_data = btc_price.json()
eth_data = eth_price.json()

btc_price = btc_data['data']['1']['quotes']['USD']['price']
eth_price = eth_data['data']['1027']['quotes']['USD']['price']

eth_price


# %%
def f(x):
    return eth_price * x


# %%
widgets.interact(f, x=(0, 100));


# %%
# Compute current value of my crpto
#my_btc_value = my_btc * btc_price

# Print current crypto wallet balance
#print(f"The current value of your {my_btc} BTC is ${my_btc_value:0.2f}")
print(f)


# %%



