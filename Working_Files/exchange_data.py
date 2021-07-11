# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Report for exchanges data. This is to help users evaluate the various exchanges that they can use to buy/sell crypto currencies

# %%
import pandas as pd
import numpy as np
from requests import api 
from pycoingecko import CoinGeckoAPI

def get_exchanges_data():

    df_exchanges_data = pd.DataFrame(columns=['Rank', 'Logo', 'ID', 'Name', 'URL', 'trade_volume_24h_btc'], index=None)
    df_exchanges_data.columns

    # The Python library pycoingecko deesnt have the method to get the exchanges data, so calling the GET request to the API instead
    
    enpoint_url = f"https://api.coingecko.com/api/v3/exchanges"
    exc_data_json = api.get(enpoint_url).json()
    exc_data_json[0]


    for a in exc_data_json:

        name = a['name']
        year = a['year_established']
        country = a['country']
        

        exc_name = f'{name} - (est. {year}), {country}'
        # print(exc_name)

        # Markdown for Logo
        image_txt = a['name']
        image_url = a['image']
        logo  = f'![{image_txt}]({image_url})'

        # Markdown for link to website
        link = a['url']
        link_txt = 'Link'
        exc_link = f'[{ link_txt }]({ link })'

        trade_vol = round(a['trade_volume_24h_btc_normalized'], 2)

        df_exchanges_data = df_exchanges_data.append(pd.Series([
            a['trust_score_rank'],
            logo,
            a['id'],
            exc_name,
            exc_link,
            trade_vol
        ], index= df_exchanges_data.columns), ignore_index= True)



    return df_exchanges_data





