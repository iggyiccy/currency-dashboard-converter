# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import pandas as pd
import numpy as np
import yfinance as yf
import panel as pn
import os
import ipywidgets as widgets
import requests
from requests import api
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt


# %%
pn.extension("plotly")
import plotly.express as px


# %%
#Country Codes
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


# %%
#Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=AUD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=AUD"

btc_url = btc_url + "?format=json"
eth_url = eth_url + "?format=json"

# %% [markdown]
# # Gathering Crypto Data

# %%
# Fetch current BTC price
btc_price = requests.get(btc_url)

# Fetch current ETH price
eth_price = requests.get(eth_url)

btc_response = btc_price.content
eth_response = eth_price.content

btc_data = btc_price.json()
eth_data = eth_price.json()

btc_price = btc_data['data']['1']['quotes']['USD']['price']
eth_price = eth_data['data']['1027']['quotes']['USD']['price']

eth_data


# %%
df = pd.DataFrame(columns=['crypto', 'USD', 'AUD'], index=None)


# %%
df = df.append(pd.Series(['ETH', eth_price, '12000'], index= df.columns), ignore_index=True)
df = df.append(pd.Series(['BTC', btc_price, '32000'], index= df.columns), ignore_index=True)
df


# %%
df.set_index('crypto', inplace=True)
df


# %%
def f(x):
#     return eth_price * x
    global df['USD'] = df['USD'] * x
    global df['AUD'] = df['AUD'] * x
    
    fig = plt.figure()

    scat = plt.scatter( )
    return 


# %%
widgets.interact(f, x=(0, 100))
output = widgets.Output()


# %%
# Compute current value of my crpto
#my_btc_value = my_btc * btc_price

# Print current crypto wallet balance
#print(f"The current value of your {my_btc} BTC is ${my_btc_value:0.2f}")
print(f)


# %%
slider = widgets.IntSlider(value=50, min=1, max=50,  continuous_update=False)
slider.style.handle_color="lawngreen"
slider


# %%
output = widgets.Output()

with output:
    with plt.style.context("ggplot"):
        fig = plt.figure()
#         scat = plt.scatter(x=iris_df[:50]['sepal length (cm)'],
#                            y=iris_df[:50]['petal length (cm)'],
#                            c=iris_df[:50]["FlowerType"]
#                           )
        plt.colorbar(df)
        plt.xlabel("sepal length (cm)".capitalize())
        plt.ylabel("petal length (cm)".capitalize())
        plt.title("sepal length (cm) vs petal length (cm) Relation")


# %%
def update_scatter_chart(new_slider_val):
    with output:
        with plt.style.context("ggplot"):
            fig = plt.figure()
#             plt.scatter(x=df.index,
#                         y=[df['USD'], df['AUD']])
            plt.colorbar(df)
            plt.xlabel("Date")
            plt.ylabel("Price ($)")
            plt.title("Line Chart for Apple Prices");
            fig.canvas.draw()

slider.observe(update_scatter_chart, names="value")


# %%
slider_label = widgets.Label("Number of Ethereum to buy")
slider_comp = widgets.HBox([slider_label, slider])
widgets.VBox([slider_comp, output])


# %%
print(np.__version__)


# %%
print(pd.__version__)


# %%
a = widgets.FloatSlider()
b = widgets.FloatText()

display(a,b)

mylink = widgets.jslink((a, 'value'), (b, 'value'))


# %%
w= interactive_plot()


# %%
get_ipython().run_line_magic('matplotlib', 'inline')
from ipywidgets import interactive
import matplotlib.pyplot as plt
import numpy as np

def f(m, b):
    plt.figure(2)
    x = np.linspace(-10, 10, num=1000)
    plt.plot(x, m * x + b)
    plt.ylim(-5, 5)
    plt.show()

interactive_plot = interactive(f, m=(-2.0, 2.0), b=(-3, 3, 0.5))
output = interactive_plot.children[-1]
output.layout.height = '350px'
interactive_plot


# %%
df_crypto = ['BTC', 'ETH', 'LTC', 'XRP']
df_curr = ['USD', 'AUD', 'EUR']


# %%



# %%



# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interactive
get_ipython().run_line_magic('matplotlib', 'inline')

columns=['a','b','c']
data = np.cumsum(np.random.rand(10,3),axis=1)
df = pd.DataFrame(data,columns=columns)

def g(x,y):
    print(x)
    print(y)
    plt.scatter(df[x], df[y])
    plt.show()

interactive_plot = interactive(g, x=columns, y=columns)
interactive_plot


# %%



