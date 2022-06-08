import yfinance as yafi
import pandas as pd


def get_data_for_ticker(ticker_name):
    """
    :param ticker_name: string containing ticker name (symbol)
    :return:
        data_for_max - json containing stock data for max years with period of 1 day
        data_for_quarter - json containing stock data for 3 months with period of 1 hour
        data_for_month - json containing stock data for 1 month with period of 1 minute
        news - newsfeed for given stock name
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

    yafi_ticker = yafi.Ticker(ticker_name)
    news = yafi_ticker.news
    info = yafi_ticker.info
    institutional_holders = yafi_ticker.institutional_holders
    calendar = yafi_ticker.calendar
    if not (data_for_max.empty & data_for_month.empty & data_for_quarter.empty):
        return data_for_max.to_json(), data_for_quarter.to_json(), data_for_month.to_json(), news, info, institutional_holders, calendar
    else:
        return None, None, None, None, None, None, None

if __name__ == "__main__":
    d1, d2, d3, news, info, holders, calendar = get_data_for_ticker("AAPL")
