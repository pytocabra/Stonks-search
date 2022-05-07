import plotly.graph_objects as go
import pandas as pd
import yfinance as yafi
from stocksymbol import StockSymbol

print("1")

api_key = "c526e7cb-b641-49e4-81f6-a855a3de479a"
ss = StockSymbol(api_key)
symbol_list_us = ss.get_symbol_list(market="US", symbols_only=True)

data = yafi.download(
        tickers = "AAPL",
        period = "1y",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )


fig = go.Figure(data=[go.Candlestick(x=data.index,
                 open=data.Open.values, high=data.High.values,
                 low=data.Low.values, close=data.Close.values)
                      ])

fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()
