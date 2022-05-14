import plotly.graph_objects as go
import pandas as pd
import yfinance as yafi
from stocksymbol import StockSymbol
import sqlite3

api_key = "c526e7cb-b641-49e4-81f6-a855a3de479a"
ss = StockSymbol(api_key)
#lista słowników...
symbol_list_us = ss.get_symbol_list(market="US", symbols_only=False)
symbol_df = pd.DataFrame(symbol_list_us)

#print(symbol_df["symbol"])


conn = sqlite3.connect("db.sqlite3")
symbol_df.to_sql("SYMBOLS", conn, if_exists="replace", index=False)

zapytanie = "\'%apple%\'"
print(pd.read_sql("select * from SYMBOLS WHERE symbol LIKE " + zapytanie + " OR longName LIKE " + zapytanie, conn))



# def check_if_valid_ticker(ticker_to_check):
#     return (ticker_to_check in symbol_list_us)
#
#
# assert check_if_valid_ticker("AAPL") == True
#
# assert check_if_valid_ticker("TEST") == False


# data = yafi.download(
#         tickers = "AAPL",
#         period = "1y",
#         interval = "1d",
#         group_by = 'ticker',
#         auto_adjust = True,
#         prepost = True,
#         threads = True,
#         proxy = None
#     )
#
#
# fig = go.Figure(data=[go.Candlestick(x=data.index,
#                  open=data.Open.values, high=data.High.values,
#                  low=data.Low.values, close=data.Close.values)
#                       ])
#
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()
