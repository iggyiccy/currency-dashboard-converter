# Cryptocurrency Converter Dashboard

FinTech Boot Camp Project 1 - 29/6/21 - 12/7/21

![](Data/demo.gif)

![bitcoin-world-map](Data/bitcoin_world_map.png)

# Project Title

The R2S2 Cryptocurrency Converter

# Team members

- Simon Sakkal
- Richard Patriquin
- Regina Chow
- Siddhesh Tungare

# Project Description/Outline

- Dashboard to display cryptocurrency rates across the world
- Currency converter interface to provide the user the feature to view current cryptocurrency prices in fiat currency, along with the price trends over recent timeframes
- Provide Crypto market updates
- Report on Crypto exchanges and their market shares

# Research Questions answered in the project

- As a world wide traveller, we are always looking for the best exchange rate and most discounted crypto currency we can get for the current country we are in
- As investors, we would like a calculator which provides the conversion rate of the crypto currency to the national currency and the recent price trends
- As a crypto investor, we are interested in visualising the price trends of the leading crypto currencies over the past few years
- As investors, we are interested in the latest crypto market updates
- As a person interested in investing in crypto, we would like to know the exchanges which facilitate crypto investing/trading opportunities

# Solution Overview

## Datasets

- Country-specific data inculding the geocode, from Kaggle.com

## Data-provider APIs

- yfinance (python librry for Yahoo! Finance)
- pyciongecko (python library for CoinGecko)
- country.io
- API Alternative V2

## Libraries used for plotting

- plotly.express
- dash
- dash_bootstrap_components

## Other libraries used

- pandas
- numpy
- requests

## Installation

create a new conda environment

```
1. conda create --name dash python=3.7
2. conda activate dash
```

run two of these command

```
1. pip install -r requirements.txt
2. python app.py
```

## Detailed documentation on individual components of dashboard

- [Local Price tab](Solution_Docos/crypto_worldwide_prices.md)
- [Analysis Tab](Solution_Docos/plot_5_years.md)
- [Converter Tab](Solution_Docos/crypto_converter.md)
- [Crypto Updates Tab](Solution_Docos/Crypto_Status_Updates.md)
- [Exchanges report Tab](Solution_Docos/Crypto_exchanges_data.md)

## Detailed documentation of the Dashboard application

- [Dash_app](Solution_Docos/dash_app.md)
