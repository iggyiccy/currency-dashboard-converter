#------------------------------------------------------ DATA CLEASING & MAP  ------------------------------------------------------

from dash_core_components.Markdown import Markdown
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

import Functions_data_graphs

#------------------------------------------------------Get the map plot-------------------------------------------------------
map1 = Functions_data_graphs.get_mapbox()

#---------------------------------------------------Get DF forstatus updates--------------------------------------------------

df_status_updates = Functions_data_graphs.get_status_updates()

#--------------------------------------------------Get DF for exchanges data--------------------------------------------------

df_exchanges_data = Functions_data_graphs.get_exchanges_data()

#-------------------------------------------------------Converter data--------------------------------------------------------

crypto_coins = ['bitcoin','ethereum','litecoin','ripple','eos','monero','stellar']
fiat = ['usd','aud','eur','gbp','cad','sgd']

df_cryp_fiat_conv = Functions_data_graphs.get_crypto_fiat_conv(  crypto_coins = crypto_coins, fiat = fiat )
#------------------------------------------------------ DASHBOARD BELOW ------------------------------------------------------

# -*- coding: utf-8 -*-

# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table


df = pd.read_csv('https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Bootstrap/Side-Bar/iranian_students.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)

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
                dbc.NavLink("Crypto Updates", href="/page-3", active="exact"),
                dbc.NavLink("Exchanges Report", href="/page-4", active="exact"),
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
        children = [
                html.H1('Cryptocurrency Price in Your Local Currency',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph', figure=map1)
        ]

        return children
    elif pathname == "/page-1":
        children = [
                html.H1('Major Cryptocurrency Trend and Analysis',
                        style={'textAlign':'center'}),
                dcc.Graph(id='bargraph',
                         figure=px.bar(df, barmode='group', x='Years',
                         y=['Girls Grade School', 'Boys Grade School']))
                ]
        return children
    elif pathname == "/page-2":
        children = [
                html.H1('Cryptocurrency Converter',
                        style={'textAlign':'center'}),
                # For the dropdown - crypto
                html.H6('Select the currency you want to buy'),
                html.Div( [
                    dcc.Dropdown(id='conv_cryp_drop',
                            options= [ 
                                {'label': i, 'value':i } for i in crypto_coins
                            ],
                            value='bitcoin',
                            multi=False,
                            clearable=False
                        ),
                    ], style={'width': '15%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5},
                    className='six columns'),

                # For the dropdown - Fiat
                html.H6('Select the Fiat currency you want to buy the crypto with'),
                html.Div( [
                    dcc.Dropdown(id='conv_fiat_drop',
                            options= [ 
                                {'label': i, 'value':i } for i in fiat
                            ],
                            value='aud',
                            multi=False,
                            clearable=False
                        ),
                    ], style={'width': '15%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5},
                    className='six columns'),

                # Input field for number of coins
                html.H6('Enter the amount of coins you want to buy'),
                html.Div( [
                    dcc.Input( id="num_crypto", 
                    type="number", 
                    debounce= True,         #This will only trigger the callback when user presses enter or elsewhere in the page
                    placeholder="Number of coins"
                    ),

                    html.Br(),
                    html.Br(),

                ], style={'width': '15%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5},
                    className='row'),

                # For the converter output, which will be text 
                html.Div(id = 'conv_text_output',
                children = [],
                # dcc.Markdown()
                style={'width': '100%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5},
                    className='row'), 

                ]
        return children
    elif pathname == "/page-3":
        children = [
                html.H1('Cryptocurrencies Status Updates',
                        style={'textAlign':'center'}),
                html.Div([
                    html.Br(),
                    html.Br(),
                    # For the dropdown
                    html.H6('Select the category to view the corresponding updates'),
                    html.Div( [
                        dcc.Dropdown(id='linedropdown',
                                options=[
                                        {'label': 'General', 'value': 'general'},
                                        {'label': 'Software Release', 'value': 'software_release'},
                                        {'label': 'Milestone', 'value': 'milestone'},
                                        {'label': 'Exchange Listing', 'value': 'exchange_listing'}
                                ],
                                value='general',
                                multi=False,
                                clearable=False
                            ),
                        ], style={'width': '15%', 'display': 'inline-block', 'marginBottom': 50, 'marginTop': 5},
                        className='six columns'),

                    # For the datatable
                    html.Div([ 
                        dash_table.DataTable(
                            id='datatable_id',
                            data=df_status_updates.to_dict('records'),
                            columns=[
                                {'name': 'Logo', 'id': 'Logo', "presentation": "markdown"},
                                {'name': 'Symbol', 'id': 'Symbol'},
                                {'name': 'Update', 'id': 'Description'},
                                {'name': 'Created at', 'id': 'Created_at'},
                                {'name': 'User', 'id': 'User'},
                            ],
                            editable=False,
                            sort_action="native",
                            sort_mode="multi",
                            row_deletable=False,
                            page_action="native",
                            page_current= 0,
                            page_size= 5,
                            style_cell={
                            'whiteSpace': 'normal',
                            'word-break': 'break-all',          # For word wrap
                            },
                            # fixed_rows={ 'headers': True, 'data': 0 },
                            # virtualization=False,
                            style_cell_conditional=[
                                {'if': {'column_id': 'Logo'},
                                'width': '10%', 'textAlign': 'left'},
                                {'if': {'column_id': 'Symbol'},
                                'width': '10%', 'textAlign': 'left'},
                                {'if': {'column_id': 'Description'},
                                'width': '50%', 'textAlign': 'left'},
                                {'if': {'column_id': 'Created_at'},
                                'width': '15%', 'textAlign': 'left'},
                                {'if': {'column_id': 'User'},
                                'width': '15%', 'textAlign': 'left'},
                            ],
                        ), 
                    ],className='row'),
                ])
                ]
        return children
    elif pathname == "/page-4":
        children = [
                html.H1('Cryptocurrencies Exchanges Report',
                        style={'textAlign':'center'}),
                html.Div([
                    html.Br(),
                    html.Br(),
                    # For the datatable
                    html.H3('This report is to provide users more information about the exchanges that they can use to buy/sell cryptocurrencies'),
                    # For the datatable
                    html.Div([ 
                        dash_table.DataTable(
                            id='exchangeTab',
                            data=df_exchanges_data.to_dict('records'),
                            columns=[
                                {'name': 'Rank', 'id': 'Rank'},
                                {'name': 'Logo', 'id': 'Logo', "presentation": "markdown"},
                                {'name': 'ID', 'id': 'ID'},
                                {'name': 'Name', 'id': 'Name'},
                                {'name': 'URL', 'id': 'URL', "presentation": "markdown"},
                                {'name': 'Trading Vol. (in USD) - 24 Hours', 'id': 'trade_volume_24h_btc'},
                            ],
                            editable=False,
                            sort_action="native",
                            sort_mode="multi",
                            row_selectable="multi",
                            row_deletable=False,
                            selected_rows=[],
                            page_action="native",
                            # page_current= 0,
                            # page_size= 5,
                            style_cell={
                            'whiteSpace': 'normal',
                            'word-break': 'break-all',
                            },
                            fixed_rows={ 'headers': True, 'data': 0 },
                            virtualization=False,
                            style_cell_conditional=[
                                {'if': {'column_id': 'Rank'},
                                'width': '10%', 'textAlign': 'center'},
                                {'if': {'column_id': 'Logo'},
                                'width': '10%', 'textAlign': 'left'},
                                {'if': {'column_id': 'ID'},
                                'width': '10%', 'textAlign': 'left'},
                                {'if': {'column_id': 'Name'},
                                'width': '45%', 'textAlign': 'left'},
                                {'if': {'column_id': 'URL'},
                                'width': '10%', 'textAlign': 'left'},
                                {'if': {'column_id': 'trade_volume_24h_btc'},
                                'width': '15%', 'textAlign': 'left'},
                            ],
                        ), 
                    ],className='six columns'),
                # For the piechart
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.H3('Comparison by trading volume'),
                    html.Div([
                        dcc.Graph(id='exchangePie'),
                    ],className='six columns'),

                ],  style={'width': '40%', 'display': 'inline-block', 'marginBottom': 50, 'marginTop': 5},
                className='row'),

                ])
                ]
        return children
    else:
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
    )

@app.callback(
    Output('datatable_id', 'data'),
    Input('linedropdown', 'value')
)
def update_status_tab(dropdown_val):
    df_filtered = df_status_updates.loc[ df_status_updates['Category'] == dropdown_val  ]
    return df_filtered.to_dict('records')

@app.callback(
    Output('exchangePie', 'figure'),
    Input('exchangeTab', 'selected_rows')
)
def update_exchange_pie(chosen_rows):
    if len(chosen_rows)!=0:
        df_exc_filterd = df_exchanges_data.loc[ df_exchanges_data.index.isin(chosen_rows) ]
    else: 
        df_exc_filterd = df_exchanges_data.loc[:4]

    pie_chart=px.pie(
            data_frame=df_exc_filterd,
            names='ID',
            values='trade_volume_24h_btc',
            hole=.3,
            labels={'ID':'ID'}
            )
    return pie_chart

@app.callback(
    Output('conv_text_output', 'children'),
    Input('conv_cryp_drop', 'value'),
    Input('conv_fiat_drop', 'value'),
    Input('num_crypto', 'value'),
)
def update_conv_price(cryp_drop, fiat_drop, num_coins ):

    # Default value will be 'NoneType'. This should only work when the user has input a number 
    if isinstance(num_coins, (int, float)):

        rate_1 = df_cryp_fiat_conv.loc[ (df_cryp_fiat_conv['crypto'] == cryp_drop) & (df_cryp_fiat_conv['fiat'] == fiat_drop)]['value']
        conv_rate = rate_1.iloc[0]

        total_price = conv_rate * num_coins

        text_1 = f'**Conversion rate**: 1 {cryp_drop} = {conv_rate} {fiat_drop}'
        text_2 = f'To buy {num_coins} {cryp_drop}, you will need {total_price:,.2f} {fiat_drop}'

        text = '''
        %s \n
        %s
        '''% (text_1, text_2)

        children = [
            # Creating a Markdown element with the text we have generated
            dcc.Markdown(text),

            # Adding another button for displaying historical prices 
            # this will trigger another callback
            html.Button('View history', id='conv_submit_hist', n_clicks=0),

            # Another div element to display the graph
            html.Div(id = 'conv_hist_graph',
                children = [],
                style={'width': '100%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5},
                    className='six columns'), 
        ]

        return children
    
    else:
        
        return [html.Br()]

@app.callback(
    Output('conv_hist_graph', 'children'),
    Input('conv_cryp_drop', 'value'),
    Input('conv_fiat_drop', 'value'),
    Input('num_crypto', 'value'),
    [Input('conv_submit_hist', 'n_clicks')],
)
def on_click(cryp_drop, fiat_drop, num_coins, button_click ):

    if button_click == 0:
        return []

    # rate_1 = df_cryp_fiat_conv.loc[ (df_cryp_fiat_conv['crypto'] == cryp_drop) & (df_cryp_fiat_conv['fiat'] == fiat_drop)]['value']
    # conv_rate = rate_1.iloc[0]

    # total_price = conv_rate * num_coins

    # text_1 = f'**Conversion rate**: 1 {cryp_drop} = {conv_rate} {fiat_drop}'
    # text_2 = f'To buy {num_coins} {cryp_drop}, you will need {total_price:,.2f} {fiat_drop}'

    # text = '''
    # %s \n
    # %s
    # '''% (text_1, text_2)

    plot = Functions_data_graphs.get_hist_chart(cryp_drop, fiat_drop, '60' )

    children = [

                dcc.Graph(id='conv_hist_chart',
                         figure=plot 
                         )
    ]

    return children


if __name__=='__main__':
    app.run_server(debug=True, port=3000)