
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

#------------------------------------------------------Get the 5 year  plot-------------------------------------------------------

plot_5_year_fig = Functions_data_graphs.plot_5_year_plot()

#-------------------------------------------------------Converter data--------------------------------------------------------

crypto_coins = ['bitcoin','ethereum','litecoin','ripple','eos','monero','stellar']
fiat = ['usd','aud','eur','gbp','cad','sgd']

df_cryp_fiat_conv = Functions_data_graphs.get_crypto_fiat_conv(  crypto_coins = crypto_coins, fiat = fiat )

#------------------------------------------------------  CONVERTER  ------------------------------------------------------

#Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=AUD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=AUD"
btc_url = btc_url + "?format=json"
eth_url = eth_url + "?format=json"
# Fetch current BTC price
btc_price = api.get(btc_url)
# Fetch current ETH price
eth_price = api.get(eth_url)
btc_response = btc_price.content
eth_response = eth_price.content
btc_data = btc_price.json()
eth_data = eth_price.json()
btc_price = btc_data['data']['1']['quotes']['USD']['price']
eth_price = eth_data['data']['1027']['quotes']['USD']['price']

# Create Dataframe for ETH and BTC
df_eth_btc = pd.DataFrame(columns=['crypto', 'USD', 'AUD'], index=None)
df_eth_btc = df_eth_btc.append(pd.Series(['ETH', eth_price, '12000'], index= df_eth_btc.columns), ignore_index=True)
df_eth_btc = df_eth_btc.append(pd.Series(['BTC', btc_price, '32000'], index= df_eth_btc.columns), ignore_index=True)
df_eth_btc.set_index('crypto', inplace=True)

#------------------------------------------------------ DASHBOARD BELOW ------------------------------------------------------

# -*- coding: utf-8 -*-

# Run this app with `python dash_app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)

server = app.server

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
    "margin-left": "24rem",
    "margin-right": "3rem",
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
                dbc.NavLink("🌍 Local Price", href="/", active="exact"),
                dbc.NavLink("💹 Analysis", href="/page-1", active="exact"),
                dbc.NavLink("💱 Converter", href="/page-2", active="exact"),
                dbc.NavLink("⏰ Crypto Updates", href="/page-3", active="exact"),
                dbc.NavLink("📋 Exchanges Report", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# define content variables
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# Style page 4 cards

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.Br(),
            html.Br(),
            html.H3('Comparison by trading volume'),
            html.Div([dcc.Graph(id='exchangePie'),]),
        ]
    )
)


second_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Alert("This report is to provide users more information about the exchanges that they can use to buy/sell cryptocurrencies.", color="primary"),
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
                    style_cell={'whiteSpace': 'normal','word-break': 'break-all',},
                    fixed_rows={ 'headers': True, 'data': 0 },
                    virtualization=False,
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'Rank'},
                                        'width': '10%', 'textAlign': 'center'},
                                        {'if': {'column_id': 'Logo'},
                                        'width': '5%', 'textAlign': 'left'},
                                        {'if': {'column_id': 'ID'},
                                        'width': '10%', 'textAlign': 'left'},
                                        {'if': {'column_id': 'Name'},
                                        'width': '45%', 'textAlign': 'left'},
                                        {'if': {'column_id': 'URL'},
                                        'width': '5%', 'textAlign': 'left'},
                                        {'if': {'column_id': 'trade_volume_24h_btc'},
                                        'width': '25%', 'textAlign': 'left'},],
                        ),
            ],)
        ]
    )
)

# Form formatting 
crypto_input = dbc.FormGroup(
    [
        dbc.Label("Cryptocurrency:", html_for="crypto_dropdown", width=2),
        dbc.Col(
            dcc.Dropdown(
                id = 'conv_cryp_drop',
                options= [{'label': i, 'value':i } for i in crypto_coins],
                value='bitcoin',
                multi=False,
                clearable=False
            ),
            width=10
        ),
    ],
    row=True,
)

fiat_input = dbc.FormGroup(
    [
        dbc.Label("Fiat Currency", html_for="fiat_dropdown", width=2),
        dbc.Col(
            dcc.Dropdown(
                id='conv_fiat_drop',
                options= [{'label': i, 'value':i } for i in fiat],
                value='aud',
                multi=False,
                clearable=False
            ),
            width=10,
        ),
    ],
    row=True,
)

amount_input = dbc.FormGroup(
    [
        dbc.Label("Amount of Crypto", html_for="amount_input", width=2),
        dbc.Col(
            dbc.Input(
                id="num_crypto",
                type="number",
                debounce= True,
                placeholder="10000"
            ),
            width=10,
        ),
    ],
    row=True,
)

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
                html.H1('🌍 Cryptocurrency Price in Your Local Currency',
                        style={'textAlign':'center'}),
                html.Br(),
                html.Hr(),
                html.Br(),
                dcc.Graph(id='map', figure=map1)
        ]

        return children
    elif pathname == "/page-1":
        children = [
                html.H1('💹 Major Cryptocurrency Trend and Analysis',
                        style={'textAlign':'center'}),
                html.Br(),
                html.Hr(),
                dcc.Graph(id='linegraph', figure=plot_5_year_fig)
        ]

        return children
    elif pathname == "/page-2":
        children = [
                html.H1('💱 Cryptocurrency Converter',
                        style={'textAlign':'center'}),
                html.Br(),
                html.Hr(),
                html.Br(),
                dbc.Alert(
                    [html.H2("Let's Start Converting!", className="alert-heading"),
                        html.P(
                            "Below is a currency converter allow you to convert from USD to "
                            "BTC or ETH instantly! Thanks to Dash's callback function, we able "
                            "to make this feature :) Have fun! 😉"
                        ),
                        html.Hr(),
                        html.P(
                            "Try fill up the form below to calculate how much you can convert:) ",
                            className="mb-0",),
                    ], color="light"),
                html.Hr(style={'border':'10px solid white'}),
                dbc.CardDeck(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Button(html.H4("$USD"), className="btn-outline-success", color="white", style={'border':'2px solid'}),
                                    html.Hr(),
                                    html.P("Input $USD amount below to convert:", className="card-text",),
                                    dbc.InputGroup([dbc.InputGroupAddon("Amount", addon_type="prepend"), dbc.Input(value=0.0, id="usd", type="number", placeholder="$1000.00", debounce=False, style={'marginRight':'10px'}, bs_size="lg")], size="lg",),
                                ]
                            )
                        , color="success", outline=True, style={'border-radius':'25px','border':'2px solid'}),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Button(html.H4("$BTC"), className="btn-outline-warning", color="white", style={'border':'2px solid'}),
                                    html.Hr(),
                                    html.P("Amount in $BTC:", className="card-text",),
                                    dbc.InputGroup([dbc.InputGroupAddon("Amount", addon_type="prepend"), dbc.Input(id="btc", type="number", placeholder=f"current price ${btc_price}", style={'marginRight':'10px', 'background':'white'}, bs_size="lg", disabled = True)], size="lg",),
                                ]
                            )
                        , color="warning", outline=True, style={'border-radius':'25px','border':'2px solid'}),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Button(html.H4("$ETH"), className="btn-outline-danger", color="white", style={'border':'2px solid'}),
                                    html.Hr(),
                                    html.P("Amount in $ETH:", className="card-text",),
                                    dbc.InputGroup([dbc.InputGroupAddon("Amount", addon_type="prepend"), dbc.Input(id="eth", type="number", placeholder=f"current price ${eth_price}", style={'marginRight':'10px', 'background':'white'}, bs_size="lg", disabled = True)], size="lg",),
                                ]
                            )
                        , color="danger", outline=True, style={'border-radius':'25px','border':'2px solid'}),
                    ]
                ),
                # For the dropdown - crypto
                html.Hr(style={'border':'10px solid white'}),
                dbc.Card(
                    [
                        dbc.CardHeader(html.H4("More! ⬇ Pick your currency, We will convert it for you! ", className="card-title")),
                        dbc.CardBody(
                            dbc.Form([crypto_input, fiat_input, amount_input, dbc.Button("Submit", outline=True, color="secondary", className="mr-1")])
                        )
                    ]),
                html.Br(),html.Br(),
                html.Div(
                    dbc.Card(
                            dbc.CardBody(id = 'conv_text_output', children = [],style={'width': '100%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5, 'text-align': 'center'}, className='row'),
                            className="mb-3",
                        ),
                    ),
                ]
        return children
    elif pathname == "/page-3":
        children = [
                html.H1('⏰ Cryptocurrencies Status Updates',
                        style={'textAlign':'center'}),
                html.Div([
                    html.Br(),
                    html.Hr(),
                    html.Br(),
                    dbc.Alert("😁 A collection of altcoins lastest news / maintainance alert / update! Everything you need in a single dashboard :)", color="info", style={'text-align': 'center'}),
                    # For the dropdown
                    html.H6('Select the category to view the corresponding updates', style = {'text-align': 'center'}),
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
                        ], style={'width': '15%', 'display': 'inline-block', 'marginBottom': 50, 'marginTop': 5, 'text-align': 'center', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'},
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
                html.H1('📋 Cryptocurrencies Exchanges Report',
                        style={'textAlign':'center'}),
                html.Br(),
                html.Hr(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(first_card, width=4),
                        dbc.Col(second_card, width=8),
                    ]
                )
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
    Output("usd", "value"),
    Output("eth", "value"),
    Output("btc", "value"),
    Input("usd", "value"),
    Input("eth", "value"),
    Input("btc", "value"),
)
def sync_input(usd, eth, btc):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "usd":
        eth = None if usd is None else (float(usd) / eth_price)
        btc = None if usd is None else (float(usd) / btc_price)
    else:
        usd = None 
    return usd, eth, btc

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

        text_1 = f'Conversion rate: 1 {cryp_drop} = {conv_rate} {fiat_drop}'
        text_2 = f'To buy {num_coins} {cryp_drop}, you will need {total_price:,.2f} {fiat_drop}'

        text = '''
        ### %s \n
        ### %s
        '''% (text_1, text_2)

        children = [
            # Creating a Markdown element with the text we have generated
            dcc.Markdown(text),html.Br(),

            # Adding another button for displaying historical prices 
            # this will trigger another callback
            dbc.Button('View history', id='conv_submit_hist', n_clicks=0, outline=True, color="secondary", className="mr-1"),

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
    heroku_port = int(os.environ.get('PORT')) 
    app.run_server(debug=True, port=heroku_port)