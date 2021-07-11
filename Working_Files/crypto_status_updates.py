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
df_status_updates = pd.DataFrame(columns=['Category', 'Thumb_url', 'Symbol', 'Description', 'Created_at', 'User'], index=None)
df_status_updates.columns

# %% [markdown]
# ## Initialise the coingecko API and request the status_updates endpoint

# %%
category = ['general', 'software_release', 'milestone', 'exchange_listing', ]

for cat in category:

    enpoint_url = f"https://api.coingecko.com/api/v3/status_updates?category={cat}&project_type=coin&per_page=5&page=1"
    status_upd_json = api.get(enpoint_url).json()
    status_upd = status_upd_json['status_updates']

    for status in status_upd:
        # print(status)
        user_name = status['user']
        user_title = status['user_title']
        user = f'{user_name} ({user_title})'

        df_status_updates = df_status_updates.append(pd.Series([
            status['category'],
            status['project']['image']['thumb'],
            status['project']['symbol'],
            status['description'],
            status['created_at'],
            user
            ], index=df_status_updates.columns), ignore_index=True)

    
# print(df_status_updates)


# %%
df_status_updates.head()


# %%
fig = go.Figure(data=[go.Table(
  columnorder = [1,2,3,4,5,6],
  columnwidth = [40,40,120, 80,80,80],
  # header = dict(
  #   values = [ ['<b>Category</b>'],['<b>Symbol</b>'], ['<b>Description</b>'], ['<b>Created at</b>'], ['<b>User</b>'], ['<b>Thumb_URL</b>'] ]
  #   # line_color='darkslategray',
  #   # fill_color='royalblue',
  #   # align=['left', 'left', 'left', 'left', 'left', 'left']
  #   # font=dict(color='white', size=12),
  #   # height=40
  # ),
  cells=dict(
    # values= df_status_updates,              #The dataframe
    values= df_status_updates
    # line_color='darkslategray',
    # fill=dict(color='paleturquoise'),
    # align= 'left',
    # font_size=12,
    # height=30
    )
    )
])


# %%
# fig.show()


# %%
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd


# %%
# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Graph(figure=fig)

# app.layout = html.Div([
#     dash_table.DataTable(
#         id='table',
#         columns=[{"name": i.str.upper(), "id": i} 
#                  for i in df_status_updates.columns],
#         data=df_status_updates.to_dict('records'),
#         style_cell=dict(textAlign='left'),
#         style_header=dict(backgroundColor="paleturquoise"),
#         style_data=dict(backgroundColor="lavender")
#     )
# ])

# app.run_server(debug=True)


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
        # dcc.Dropdown(id='linedropdown',
        #             options=[
        #                     {'label': 'General', 'value': 'general'},
        #                     {'label': 'Software Release', 'value': 'software_release'},
        #                     {'label': 'Milestone', 'value': 'milestone'},
        #                     {'label': 'Exchange Listing', 'value': 'exchange_listing'}
        #             ],
        #             value='general',
        #             multi=False,
        #             clearable=False
        #         ),
        
        
        dash_table.DataTable(
            id='datatable_id',
            data=df_status_updates.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in df_status_updates.columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            # row_selectable="multi",
            row_deletable=False,
            # selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'Category'},
                 'width': '12%', 'textAlign': 'left'},
                {'if': {'column_id': 'Thumb_url'},
                 'width': '12%', 'textAlign': 'left'},
                {'if': {'column_id': 'Symbol'},
                 'width': '12%', 'textAlign': 'left'},
                {'if': {'column_id': 'Description'},
                 'width': '40%', 'textAlign': 'left'},
                {'if': {'column_id': 'Created_at'},
                 'width': '12%', 'textAlign': 'left'},
                {'if': {'column_id': 'User'},
                 'width': '12%', 'textAlign': 'left'},
            ],
        ), 
    ],className='row'),

])

# #------------------------------------------------------------------
# @app.callback(
#     [Output('datatable_id', 'figure'),
#      Output('linechart', 'figure')],
#     [Input('datatable_id', 'selected_rows'),
#      Input('piedropdown', 'value'),
#      Input('linedropdown', 'value')]
# )
# def update_data(chosen_rows,piedropval,linedropval):




if __name__ == '__main__':
    app.run_server(debug=True)