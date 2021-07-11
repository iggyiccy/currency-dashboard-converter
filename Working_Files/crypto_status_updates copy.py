# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
from requests import api 
from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go

# %% [markdown]
# ## Defining the dataframes to store the status updates

# %%
df_status_updates = pd.DataFrame(columns=['Category', 'Logo', 'Symbol', 'Description', 'Created_at', 'User'], index=None)
df_status_updates.columns

# %% [markdown]
# ## Initialise the coingecko API and request the status_updates endpoint

# %%
category = ['general', 'software_release', 'milestone', 'exchange_listing', ]

for cat in category:

    enpoint_url = f"https://api.coingecko.com/api/v3/status_updates?category={cat}&project_type=coin&per_page=20&page=1"
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

    


# %%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

# %%
app = dash.Dash(__name__)
app.layout = html.Div([

    # For the dropdown
    html.Div([
        html.H3('Select the category to view the corresponding updates'),
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
            ], style={'width': '10%', 'display': 'inline-block', 'marginBottom': 50, 'marginTop': 5},
            className='six columns'),

        ],className='row'),

    # For the datatable
    html.Div([ 
        html.H3(''),
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
            # columns=[
            #     {"name": i, "id": i, "selectable": False, "presentation": "markdown"} for i in df_status_updates.columns
            # ],
            editable=False,
            sort_action="native",
            sort_mode="multi",
            row_deletable=False,
            page_action="native",
            page_current= 0,
            page_size= 6,
            style_cell={
            'whiteSpace': 'normal',
            'word-break': 'break-all',
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

#------------------------------------------------------------------
@app.callback(
    Output('datatable_id', 'data'),
    Input('linedropdown', 'value')
)
def update_data(dropdown_val):

    df_filtered = df_status_updates.loc[ df_status_updates['Category'] == dropdown_val  ]

    return df_filtered.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)