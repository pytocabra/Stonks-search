import yfinance as yafi
import pandas as pd
import json
import numpy as np

def format_for_graph(dataframe):
    del(dataframe['Volume'])
    dataframe.loc[:, ["Open", "High", "Low", "Close"]]
    dataframe.index = dataframe.index.astype(int) // 10 ** 9
    dataframe_to_dict_with_arrays = dataframe.T.to_dict('list')
    dataframe_to_json = pd.DataFrame.from_dict(dataframe_to_dict_with_arrays)
    dataframe_to_json = dataframe_to_json.round(2).to_json()
    return dataframe_to_json


def get_data_for_ticker(ticker_name):
    """
    :param ticker_name: string containing ticker name (symbol)
    :return:
        5 element array containing following data under successive indexes:
            data_for_max_json - json containing stock data [open,close,min,max] for max years with period of 1 day
            news - newsfeed for given stock name
            info - various data for given stock
            institutional_holders - list of the biggest institutional holders
            data_for_max_close_only_json - json containing stock close value for max years with period of 1 day
    """
    data_for_max = yafi.download(
        tickers=ticker_name,
        period="1y",
        interval="1d",
        group_by='ticker',
        auto_adjust=True,
        prepost=True,
        threads=True,
        proxy=None
    )
    # percent_date_change = data_for_max['Close'].pct_change().tail(1).to_json(orient='records')[1:-1]
    percent_date_change = data_for_max['Close'].pct_change().tail(1).iloc[0]
    yesterdays_close = data_for_max['Close'].tail(1).iloc[0]
    is_rising = True if data_for_max['Close'].pct_change().tail(1).iloc[0] > 0 else False
    # print("Close: {}, Change: {}, Rising: {}".format(percent_date_change,yesterdays_close,is_rising))

    data_for_max_json = format_for_graph(data_for_max)

    data_for_max_close_only_json = data_for_max['Close'].round(2).to_json

    yafi_ticker = yafi.Ticker(ticker_name)
    news = yafi_ticker.news
    info = yafi_ticker.info

    institutional_holders = yafi_ticker.institutional_holders
    institutional_holders['Date Reported'] = institutional_holders['Date Reported'].dt.strftime('%Y-%m-%d')
    institutional_holders.rename(columns = {'Date Reported': 'DateReported', '% Out': 'Out'}, inplace = True)



    list_of_ticker_data = [data_for_max_json,
                           news,
                           info,
                           institutional_holders,
                           data_for_max_close_only_json,
                           percent_date_change,
                           yesterdays_close,
                           is_rising
                           ]

    if not (data_for_max.empty):
        return list_of_ticker_data
    else:
        return None


def get_values_for_liked_tickers(tickers_list):
    ticker_string = " ".join(tickers_list)
    # data = yafi.download(ticker_string, period="1d", interval="1m")
    data = yafi.download(ticker_string, period="2d", interval="1d")
    data.sort_index
    values_of_liked_tickers = data["Close"].tail(1).to_json(orient='records')[1:-1]
    change_of_liked_tickers = data.pct_change()["Close"].tail(1).to_json(orient='records')[1:-1]
    return values_of_liked_tickers, change_of_liked_tickers


if __name__ == "__main__":
    dane = get_data_for_ticker("AAPL")