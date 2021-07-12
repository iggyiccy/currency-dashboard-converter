dbc.Card(
                    [
                        dbc.CardHeader(html.H4("More! ⬇ Pick your currency, We will convert it for you! ", className="card-title")),
                        dbc.CardBody(
                            [dbc.Form([
                                dbc.FormGroup([
                                dbc.Label("Cryptocurrency:", html_for="dropdown"),
                                dcc.Dropdown(
                                            options= [{'label': i, 'value':i } for i in crypto_coins],
                                            value='bitcoin',
                                            multi=False,
                                            clearable=False),], style={'width': '15%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5}, className='six columns'),
                                ]),
                            ]
                        ),
                    ], color="primary", outline=True, style={'border-radius':'25px','border':'2px solid'}
                ),


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
                    

crypto_input = dbc.FormGroup(
    [
        dbc.Label("Cryptocurrency:", html_for="crypto_dropdown", width=2),
        dbc.Col(
            dbc.Dropdown(
                options= [{'label': i, 'value':i } for i in crypto_coins],
                value='bitcoin',
                multi=False,
                clearable=False)
            ),
            width=10,
        ),
    ],
    row=True,
)

fiat_input = dbc.FormGroup(
    [
        dbc.Label("Fiat Currency", html_for="fiat_dropdown", width=2),
        dbc.Col(
            dbc.Dropdown(
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


form = dbc.Form([crypto_input, fiat_input, amount_input, dbc.Button("Submit", color="primary")])


dbc.Card(
            dbc.CardBody(id = 'conv_text_output', children = [],style={'width': '100%', 'display': 'inline-block', 'marginBottom': 25, 'marginTop': 5}, className='row'),
            className="mb-3",
        ),