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
