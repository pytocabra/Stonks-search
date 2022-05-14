import plotly.graph_objects as go
import pandas as pd
import yfinance as yafi
from stocksymbol import StockSymbol
import sqlite3
import logging

API_KEY = "c526e7cb-b641-49e4-81f6-a855a3de479a"


##TODO: market_list = ss.market_list da się pobrać wszystkie Rynki... Czy chcemy pobrać dla wszystkich?
def update_ticker_database():
    ss = StockSymbol(API_KEY)
    symbols_dataframe = pd.DataFrame(ss.get_symbol_list(market="US", symbols_only=False))
    try:
        with sqlite3.connect("db.sqlite3") as symbol_db_connection:
            symbols_dataframe.to_sql("SYMBOLS", symbol_db_connection, if_exists="replace", index=False)
    except sqlite3.Error as error:
        logging.error("Error while connecting to sqlite", error)


def get_matching_tickers_from_database(given_string):
    try:
        with sqlite3.connect("db.sqlite3") as symbol_db_connection:
            match_for_given_string = "\'%{}%\'".format(given_string)
            db_query = "select * from SYMBOLS WHERE symbol LIKE {} OR longName LIKE {}".format(match_for_given_string,
                                                                                               match_for_given_string)
            cursor = symbol_db_connection.execute(db_query)
            return cursor
    except sqlite3.Error as error:
        logging.error("Error while connecting to sqlite", error)



if __name__ == "__main__":
    update_ticker_database()
    data = get_matching_tickers_from_database("apple")
    for row in data:
        print(row)