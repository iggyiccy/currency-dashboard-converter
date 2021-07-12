import yfinance as yf
import os  
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import panel as pn
from requests import api 
from pycoingecko import CoinGeckoAPI

df_ticker_low = yf.download(['BTC-USD' , 'ETH-USD', 'DOGE-USD', 'ADA-USD', 'MATIC-USD'], period='5y', group_by= 'ticker', dtype= object)

df_closing_prices = pd.DataFrame()
df_closing_prices["BTC"] = df_ticker_low["BTC-USD"]["Close"]
df_closing_prices["ETH"] = df_ticker_low["ETH-USD"]["Close"]
df_closing_prices["DOGE"] = df_ticker_low["DOGE-USD"]["Close"]
df_closing_prices["ADA"] = df_ticker_low["ADA-USD"]["Close"]
df_closing_prices["MATIC"] = df_ticker_low["MATIC-USD"]["Close"]
df_closing_prices.index = df_ticker_low.index.date

df_closing_prices.to_csv('Data/df_closing_prices.csv')