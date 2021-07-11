# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#This is coding which imports the necessary libraries and API's required to retrieve and plot the data.
import pandas as pd
import numpy as np
import yfinance as yf
import panel as pn
import os
from requests import api 
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI


# %%
#This is coding which imports the necessary libraries and API's required to retrieve and plot the data.
pn.extension("plotly")
import plotly.express as px


# %%
#Code to import and download 5 years worth of pricing data (USD) for Bitcoin (BTC), Etherium (ETH), Dogecoin (DOGE), Cardano (ADA) and Polygon (MATIC).
df_ticker_low = yf.download(['BTC-USD' , 'ETH-USD', 'DOGE-USD', 'ADA-USD', 'MATIC-USD'], period='5y', group_by= 'ticker', dtype= object)
df_ticker_low


# %%
# Coding to create a new data which displays only closing prices for BTC, ETH, DOGE, ADA and MATIC
df_closing_prices = pd.DataFrame()
df_closing_prices["BTC"] = df_ticker_low["BTC-USD"]["Close"]
df_closing_prices["ETH"] = df_ticker_low["ETH-USD"]["Close"]
df_closing_prices["DOGE"] = df_ticker_low["DOGE-USD"]["Close"]
df_closing_prices["ADA"] = df_ticker_low["ADA-USD"]["Close"]
df_closing_prices["MATIC"] = df_ticker_low["MATIC-USD"]["Close"]
df_closing_prices.index = df_ticker_low.index.date
df_closing_prices


# %%
# Coding to generate a line plot of the data
df_closing_prices_plot = df_closing_prices.plot(figsize=(20, 10),title="5 year closing price history")


