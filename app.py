#------------------------------------------------------ DATA CLEASING & MAP  ------------------------------------------------------

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
## mapbox_style = "mapbox://styles/mapbox/cjcunv5ae262f2sm9tfwg8i0w"
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

#------------------------------------------------------ DASHBOARD BELOW ------------------------------------------------------

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

#------------------------------------------------------ Styling ------------------------------------------------------

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

#------------------------------------------------------ Define Components ------------------------------------------------------

# define sidebar variables
sidebar = html.Div(
    [
        html.H2("Currency Convertor", className="display-4"),
        html.Hr(),
        html.P(
            "FinTech Boot Camp Project 1 Presentation", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Local Price", href="/", active="exact"),
                dbc.NavLink("Analysis", href="/page-1", active="exact"),
                dbc.NavLink("Converter", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# define content variables
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

#------------------------------------------------------ APP ------------------------------------------------------ 

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

#------------------------------------------------------ Callbacks ------------------------------------------------------

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Cryptocurrency Price in Your Local Currency',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph', figure=map1)
                ]
    elif pathname == "/page-1":
        return [
                html.H1('Major Cryptocurrency Trend and Analysis',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls Grade School', 'Boys Grade School']))
                ]
    elif pathname == "/page-2":
        return [
                html.H1('Cryptocurrency Converter',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls High School', 'Boys High School']))
                ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__=='__main__':
    app.run_server(debug=True, port=3000)