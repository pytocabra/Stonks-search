import yfinance as yafi
import pandas as pd
import json
import numpy as np

def format_for_graph(dataframe):
    del(dataframe['Volume'])
    dataframe.loc[:, ["Open", "High", "Low", "Close"]]
    print(dataframe.head())
    dataframe.index = dataframe.index.astype(int) // 10 ** 9
    dataframe_to_dict_with_arrays = dataframe.T.to_dict('list')
    dataframe_to_json = pd.DataFrame.from_dict(dataframe_to_dict_with_arrays)
    return dataframe_to_json

def get_data_for_ticker(ticker_name):
    """
    :param ticker_name: string containing ticker name (symbol)
    :return:
        9 element array containing following data under successive indexes:
            data_for_max_json - json containing stock data [open,close,min,max] for max years with period of 1 day
            data_for_quarter_json - json containing stock data [open,close,min,max] for 3 months with period of 1 hour
            data_for_month_json - json containing stock data [open,close,min,max] for 1 month with period of 1 minute
            news - newsfeed for given stock name
            info - various data for given stock
            institutional_holders - list of the biggest institutional holders
            data_for_max_close_only_json - json containing stock close value for max years with period of 1 day
            data_for_quarter_close_only_json - json containing stock close value for 3 months with period of 1 hour
            data_for_month_close_only_json - json containing stock close value for 1 month with period of 1 minute
    """
    data_for_max = yafi.download(
        tickers=ticker_name,
        period="max",
        interval="1d",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
    )

    data_for_quarter = yafi.download(
        tickers=ticker_name,
        period="3m",
        interval="1h",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
    )

    data_for_month = yafi.download(
        tickers=ticker_name,
        period="1m",
        interval="1m",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
    )

    data_for_max_json = format_for_graph(data_for_max)
    data_for_quarter_json = format_for_graph(data_for_quarter)
    data_for_month_json = format_for_graph(data_for_month)

    data_for_max_close_only_json = data_for_max['Close'].to_json
    data_for_quarter_close_only_json = data_for_quarter['Close'].to_json
    data_for_month_close_only_json = data_for_month['Close'].to_json

    yafi_ticker = yafi.Ticker(ticker_name)
    news = yafi_ticker.news
    info = yafi_ticker.info
    institutional_holders = yafi_ticker.institutional_holders

    list_of_ticker_data = [data_for_max_json,
                           data_for_quarter_json,
                           data_for_month_json,
                           news,
                           info,
                           institutional_holders,
                           data_for_max_close_only_json,
                           data_for_quarter_close_only_json,
                           data_for_month_close_only_json]

    if not (data_for_max.empty & data_for_month.empty & data_for_quarter.empty):
        return list_of_ticker_data
    else:
        return None


if __name__ == "__main__":
    dane = get_data_for_ticker("AAPL")
    print(dane[0])