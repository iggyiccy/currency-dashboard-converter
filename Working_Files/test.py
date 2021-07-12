import pandas as pd
import numpy as np
import yfinance as yf
import panel as pn
import plotly.express as px
import os  
import requests
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI
pn.extension("plotly")

#Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=AUD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=AUD"
btc_url = btc_url + "?format=json"
eth_url = eth_url + "?format=json"
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

#Create Dataframe for ETH and BTC
df_eth_btc = pd.DataFrame(columns=['crypto', 'USD', 'AUD'], index=None)
df_eth_btc = df_eth_btc.append(pd.Series(['ETH', eth_price, '12000'], index= df_eth_btc.columns), ignore_index=True)
df_eth_btc = df_eth_btc.append(pd.Series(['BTC', btc_price, '32000'], index= df_eth_btc.columns), ignore_index=True)
df_eth_btc.set_index('crypto', inplace=True)

print(df_eth_btc.head())