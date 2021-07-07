# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
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

# %% [markdown]
# ## Get the national currencies for countries

# %%
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

# %% [markdown]
# # Get the countries data - geocodes, currency codes, etc, saved in a CSV - concap.csv

# %%
df_country_geocodes = pd.read_csv('Data/concap.csv', index_col=None)
df_country_geocodes.dropna(inplace=True)
df_country_geocodes.set_index('CountryCode', inplace=True)

# %% [markdown]
# # Concatenate the 2 DFs together to have the data in the foll, format:
# CountryCode|CountryName|CapitalName|CapitalLatitude|CapitalLongitude|ContinentName|Curr_code
# ---|---|---|---|---|---|---|
# AU|Australia|Canberra|-35.2667|149.133|Australia|AUD

# %%
df_country_data = pd.concat([df_country_geocodes, df_country_currency], axis='columns', join='inner')
df_country_data.loc['AU']


# %%
# Saving the data to CSV, we can just start with the CSVs in the final project code
df_country_data.to_csv('Data/Country_data.csv')

# %% [markdown]
# ## Just a test to display the data obtained so far

# %%
load_dotenv()
map_box_api = os.getenv("MAPBOX_PUBLIC")

# Set the Mapbox API
px.set_mapbox_access_token(map_box_api)


# %%
hover_data = {'ContinentName': False, 'CountryName':False, 'CapitalLatitude':False, 'CapitalLongitude':False, 'Curr_code':True}

map1 = px.scatter_mapbox(
    df_country_data,
    lat="CapitalLatitude",
    lon="CapitalLongitude",
    color="ContinentName",
    hover_name='CountryName',
    hover_data= hover_data, #['CapitalName', 'Curr_code' ],
    zoom = 1,
    mapbox_style='basic'
)
map1.show()


# %%
df_country_data.loc[df_country_data.Curr_code == 'DOP']

# %% [markdown]
# # Getting the crypto data - This will be used in the final project code

# %%
# form the list of fiat currencies - We need to use this to call the coingecko API
fiat = df_country_data.Curr_code.to_list()


# %%
gecko = CoinGeckoAPI()
crypto_prices = gecko.get_price(ids=['bitcoin','litecoin', 'ripple'], vs_currencies=fiat, include_market_cap=True, include_24hr_vol=True, include_24hr_change=True)


# %%
df_gecko_data = pd.DataFrame.from_dict(crypto_prices)
df_gecko_data.index = df_gecko_data.index.str.upper()
df_gecko_data.head()

# %% [markdown]
# ## We will be forming 3 DFs frmom the data received
# 
# 1. df_cryp_prices: will have the currency codes as the index, columns as the crypto names, and will store the current prices
# 
# 2. df_cryp_change: will have the currency codes as the index, columns as the crypto names, and will store the changes over 24Hours. There will also be a col for Average change
# 
# 3. df_cryp_vol: will have the currency codes as the index, columns as the crypto names, and will store the volume over 24Hours. There will also be a col for Average volume

# %%
crypto_names = df_gecko_data.columns.to_list()


# %%
df_cryp_prices = pd.DataFrame(columns= (['Curr'] + crypto_names)).set_index('Curr')

cols_change =['Curr']
for a in crypto_names: cols_change += [f'{a}_chg']
cols_change += ['Score_chg']
df_cryp_change = pd.DataFrame(columns=cols_change)

cols_vol =['Curr']
for a in crypto_names:  cols_vol += [f'{a}_vol']
cols_vol += ['Score_vol']
df_cryp_vol = pd.DataFrame(columns= cols_vol)
df_cryp_vol.columns

# %% [markdown]
# ### Populate the dataframes

# %%
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


# %%
df_cryp_change.set_index('Curr', inplace= True)
df_cryp_vol.set_index('Curr', inplace= True)
print(df_cryp_prices.head())
print(df_cryp_change.head())
print(df_cryp_vol.head())


# %%
(1.119524e+11 + 1.328155e+10 +  9.443507e+09 ) / 3


# %%
df_crypto_complete = pd.concat([df_cryp_prices, df_cryp_change, df_cryp_vol], axis='columns', join='inner')


# %%
print(df_crypto_complete.head())

# %% [markdown]
# ## Forming the dataframe which can be sent for plotting

# %%
col_names_plotting = ['Curr'] + crypto_names + ['Score_chg', 'Score_vol']
df_crypto_print = pd.DataFrame(columns= col_names_plotting)
df_crypto_print


# %%
for row in df_crypto_complete.index:
    
    row_print = [row]
    
    for name in crypto_names:
        
        col_name = name
        
        price_val = df_crypto_complete.loc[row][col_name]
        
        change_val = df_crypto_complete.loc[row][f'{col_name}_chg']
        
        vol_val = df_crypto_complete.loc[row][f'{col_name}_vol']
        
        price = "Price: {:,.2f}".format(price_val) + ", Change: {:,.2f}".format(change_val) + ", Volume: {:,.2f}".format(vol_val)
        
        row_print += [price]
#         print(price)
        
    row_print += [df_crypto_complete.loc[row]['Score_chg']] + [df_crypto_complete.loc[row]['Score_vol']] 
#     print(row_print)
    df_crypto_print = df_crypto_print.append(pd.Series(row_print, index= df_crypto_print.columns), ignore_index=True)


# %%
df_crypto_print.set_index('Curr', inplace= True)


# %%
print(df_crypto_print.head())


# %%



# %%
df_plot = df_country_data.merge(df_crypto_print, left_on='Curr_code', right_index=True, how='inner')


# %%
df_plot.head()


# %%
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
map1.show()


# %%


map2 = px.scatter_mapbox(
    df_plot,
    lat="CapitalLatitude",
    lon="CapitalLongitude",
    color="ContinentName",
    size='Score_vol',
    hover_name='CountryName',
    hover_data= hover_data, #['CapitalName', 'Curr_code' ],
    zoom = 1,
    mapbox_style='basic'
)

map1.show()


# %%



# %%



# %%



# %%



# %%



# %%
# Adding columns to the dataframe
col_zero = [0] * len(df_prices)
cols = df_prices.columns
for s in cols:
    col_name = f'{s}_24H_CHANGE'
    df_prices[col_name] = col_zero

df_prices['Score'] = col_zero
df_prices.head()
# df_prices.loc[df_prices.index ]


# %%
# just trying to search for all rows which have the pattern *_24H_CHANGE
import re
df_prices.loc[df_prices.index.str.contains('_24H_CHANGE')]


# %%
# Setting the change values in the dataframe
import re

index = 0
for c in cols:
    for row in df_prices.index:
        if len(row) == 3:
            curr = row
            new_col_name = f'{c}_24H_CHANGE'
            df_prices.loc[row,new_col_name] = df_prices.loc[f'{curr}_24H_CHANGE', c]
#                 print(new_col_name)

for row in df_prices.index:
    
    total = 0
    num = 0
    
    for c in df_prices.columns:
        
#         if c.contains('_24H_CHANGE'):
        if re.search('.+_24H_CHANGE', c) :
            total += df_prices.loc[row, c]
            num += 1
    
    
    df_prices.loc[row, 'Score'] = total / num


# %%
df_prices.head()


# %%
df_prices.loc[df_prices.index.str.contains('_24H_CHANGE')]


# %%
df_country_data.head()


# %%
# df_concatenated = pd.concat([df_country_data, df_prices], )


# %%
df_concat = df_country_data.merge(df_prices, left_on='Curr_code', right_index=True, how='inner')


# %%
(-5.177703 + -4.284477 + -6.774659 ) / 3


# %%
hover_data = {'ContinentName': False, 'CountryName':False, 'CapitalLatitude':False, 'CapitalLongitude':False, 'Curr_code':True,
             'bitcoin': True, 'litecoin':True, 'bitcoin_24H_CHANGE': True, 'litecoin_24H_CHANGE': True}

map1 = px.scatter_mapbox(
    df_concat,
    lat="CapitalLatitude",
    lon="CapitalLongitude",
    color="ContinentName",
    hover_name='CountryName',
    hover_data= hover_data, #['CapitalName', 'Curr_code' ],
    zoom = 1,
    mapbox_style='basic'
)
map1.show()


# %%



