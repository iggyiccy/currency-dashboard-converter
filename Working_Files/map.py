import pandas as pd
import numpy as np
import yfinance as yf
import panel as pn
import plotly.express as px
import os  
from requests import api 
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI
pn.extension("plotly")

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
mapbox_style = "mapbox://styles/mapbox/cjcunv5ae262f2sm9tfwg8i0w"
px.set_mapbox_access_token(mapbox_access_token)

########  ----- Get the countries data - geocodes, currency codes, etc, saved in a CSV - concap.csv  -----

country_currency = api.get('http://country.io/currency.json').json()
df_country_currency = pd.DataFrame(columns=['Code', 'Curr_code'], dtype=object)
for key,value in country_currency.items():
    df_country_currency = df_country_currency.append(pd.Series(
    [
        key,
        value
    ], index= df_country_currency.columns ), ignore_index=True)
df_country_currency.set_index('Code',inplace=True)

df_country_geocodes = pd.read_csv('Data/concap.csv', index_col=None)
df_country_geocodes.dropna(inplace=True)
df_country_geocodes.set_index('CountryCode', inplace=True)

########  ----- Concatenate the 2 DFs together to have the data in the foll, format:  -----
df_country_data = pd.concat([df_country_geocodes, df_country_currency], axis='columns', join='inner')

########  ----- Getting the crypto data - This will be used in the final project code  -----
fiat = df_country_data.Curr_code.to_list()
gecko = CoinGeckoAPI()
crypto_prices = gecko.get_price(ids=['bitcoin','litecoin', 'ripple'], vs_currencies=fiat, include_market_cap=True, include_24hr_vol=True, include_24hr_change=True)
df_gecko_data = pd.DataFrame.from_dict(crypto_prices)
df_gecko_data.index = df_gecko_data.index.str.upper()

########  ----- Forming 3 DFs (df_cryp_prices, df_cryp_change, df_cryp_vol) frmom the data received  -----
crypto_names = df_gecko_data.columns.to_list()

df_cryp_prices = pd.DataFrame(columns= (['Curr'] + crypto_names)).set_index('Curr')

cols_change =['Curr']
for a in crypto_names: cols_change += [f'{a}_chg']
cols_change += ['Score_chg']

df_cryp_change = pd.DataFrame(columns=cols_change)

cols_vol =['Curr']
for a in crypto_names:  cols_vol += [f'{a}_vol']
cols_vol += ['Score_vol']

df_cryp_vol = pd.DataFrame(columns= cols_vol)

row_2 = []
for row in df_gecko_data.index:
    
    row_data = df_gecko_data.loc[row]
    
    if len(row) == 3:
        df_cryp_prices = df_cryp_prices.append(row_data)
        
    elif '_24H_CHANGE' in row:
        row_2 = [row[0:3]]
        row_2.extend(row_data)
        avg = np.average(row_data)
        row_2.extend([np.average(row_data)])
        
        df_cryp_change = df_cryp_change.append(pd.Series(row_2, index= df_cryp_change.columns), ignore_index=True)
        
    elif '_24H_VOL' in row:
        row_2 = [row[0:3]]
        row_2.extend(row_data)
        avg = np.average(row_data)
        row_2.extend([np.average(row_data)])
        
        df_cryp_vol = df_cryp_vol.append(pd.Series(row_2, index= df_cryp_vol.columns), ignore_index=True)

df_cryp_change.set_index('Curr', inplace= True)
df_cryp_vol.set_index('Curr', inplace= True)

df_crypto_complete = pd.concat([df_cryp_prices, df_cryp_change, df_cryp_vol], axis='columns', join='inner')

########  ----- Forming the dataframe which can be sent for plotting  -----

col_names_plotting = ['Curr'] + crypto_names + ['Score_chg', 'Score_vol']
df_crypto_print = pd.DataFrame(columns= col_names_plotting)

for row in df_crypto_complete.index:
    row_print = [row]
    for name in crypto_names:
        col_name = name
        price_val = df_crypto_complete.loc[row][col_name]
        change_val = df_crypto_complete.loc[row][f'{col_name}_chg']
        vol_val = df_crypto_complete.loc[row][f'{col_name}_vol']
        price = "Price: {:,.2f}".format(price_val) + ", Change: {:,.2f}".format(change_val) + ", Volume: {:,.2f}".format(vol_val)
        row_print += [price]     
    row_print += [df_crypto_complete.loc[row]['Score_chg']] + [df_crypto_complete.loc[row]['Score_vol']] 
    df_crypto_print = df_crypto_print.append(pd.Series(row_print, index= df_crypto_print.columns), ignore_index=True)

df_crypto_print.set_index('Curr', inplace= True)

df_plot = df_country_data.merge(df_crypto_print, left_on='Curr_code', right_index=True, how='inner')

hover_data = {'ContinentName': False, 'CountryName':False, 'CapitalLatitude':False, 'CapitalLongitude':False, 'Curr_code':True,
              'ripple': True, 'bitcoin': True, 'litecoin':True}

map1 = px.scatter_mapbox(
    df_plot,
    lat="CapitalLatitude",
    lon="CapitalLongitude",
    color="ContinentName",
    hover_name='CountryName',
    hover_data= hover_data, #['CapitalName', 'Curr_code' ],
    zoom = 2,
    mapbox_style='basic',
    height=1000
)

def show_map(): 
    map1 = px.scatter_mapbox(
        df_plot,
        lat="CapitalLatitude",
        lon="CapitalLongitude",
        color="ContinentName",
        hover_name='CountryName',
        hover_data= hover_data, #['CapitalName', 'Curr_code' ],
        zoom = 2,
        mapbox_style='basic',
        height=1000)
