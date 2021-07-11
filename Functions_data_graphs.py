import pandas as pd
import numpy as np
from requests import api 
from pycoingecko import CoinGeckoAPI
import panel as pn
import plotly.express as px
import os  
pn.extension("plotly")


def get_mapbox():
    mapbox_access_token = "pk.eyJ1IjoiaWdneWljY3kiLCJhIjoiY2txeXJjMHM3MHo0ZjJ4cGoyanJ2Z2oweiJ9.Xw5mIyFuzqCf7palpJk8Jw"
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
        color="Score_chg",
        hover_name='CountryName',
        hover_data= hover_data, #['CapitalName', 'Curr_code' ],
        zoom = 2,
        mapbox_style='mapbox://styles/mapbox/cjcunv5ae262f2sm9tfwg8i0w',
        height=1000
    )

    return map1 

def get_status_updates():
    df_status_updates = pd.DataFrame(columns=['Category', 'Logo', 'Symbol', 'Description', 'Created_at', 'User'], index=None)
    df_status_updates.columns

    category = ['general', 'software_release', 'milestone', 'exchange_listing']

    for cat in category:

        enpoint_url = f"https://api.coingecko.com/api/v3/status_updates?category={cat}&project_type=coin&per_page=8&page=1"
        status_upd_json = api.get(enpoint_url).json()
        status_upd = status_upd_json['status_updates']

        for status in status_upd:
            # print(status)
            user_name = status['user']
            user_title = status['user_title']
            user = f'{user_name} ({user_title})'

            image_txt = status['project']['symbol']
            image_url = status['project']['image']['small']
            thumb = f'![{image_txt}]({image_url})'

            df_status_updates = df_status_updates.append(pd.Series([
                status['category'],
                thumb,          #status['project']['image']['thumb'],
                status['project']['symbol'],
                status['description'],
                status['created_at'],
                user
                ], index=df_status_updates.columns), ignore_index=True)

    return df_status_updates


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

def get_crypto_fiat_conv(crypto_coins, fiat):

    # Commenting this. Will be passed through the interface
    # crypto_coins = ['bitcoin','ethereum','litecoin','ripple','eos','monero','stellar']
    # fiat = ['usd','aud','eur','gbp','cad','sgd']

    crypto_str = ''
    for i in crypto_coins:
        crypto_str = crypto_str + i + ','

    fiat_str = ''
    for i in fiat:
        fiat_str = fiat_str + i + ','

    crypto_str = crypto_str[:-1]
    fiat_str = fiat_str[:-1]

    # The Python library pycoingecko deesnt have the method to get the exchanges data, so calling the GET request to the API instead
    
    enpoint_url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_str}&vs_currencies={fiat_str}"
    exc_data_json = api.get(enpoint_url).json()

    df_prices_curr = pd.DataFrame(columns=['crypto', 'fiat', 'value'], index=None) 

    for cryp in crypto_coins:

        for f in fiat:
            # print(f)
            # print(exc_data_json[cryp][f])

            df_prices_curr = df_prices_curr.append(pd.Series([
                cryp ,
                f, 
                exc_data_json[cryp][f]
            ], index= df_prices_curr.columns), ignore_index=True)

    return df_prices_curr

def get_hist_chart(coin, curr, days='60'):

    # Initialise the CoingGeckoAPI object 
    gecko = CoinGeckoAPI()

    # Calling the API 
    data = gecko.get_coin_market_chart_by_id( coin, vs_currency= curr, days= days )

    # Creating a dataframe from the data received
    df_data = pd.DataFrame(columns=['date', 'close'], index=None)

    for i in data['prices']:

        df_data = df_data.append(pd.Series([
            i[0],
            i[1]
        ], index=df_data.columns), ignore_index= True)

    # Converting from the unix timestamp 
    df_data['date'] = pd.to_datetime( df_data['date'], unit='ms', origin='unix' ) 

    # Creating the plot 
    title = f'{days} days chart of {coin} - {curr} prices' 
    fig = px.line(df_data, x='date', y="close", title= title )

    return fig

