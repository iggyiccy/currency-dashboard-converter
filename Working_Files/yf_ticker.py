import yfinance as yf
import os  
from dotenv import load_dotenv

df_ticker_low = yf.download(['BTC-USD' , 'ETH-USD', 'DOGE-USD', 'ADA-USD', 'MATIC-USD'], period='5y', group_by= 'ticker', dtype= object)
df_ticker_low.to_csv('Data/df_ticker_low.csv')