import pandas as pd
from stocksymbol import StockSymbol
from .models import StockTickerData

def clear_table():
    StockTickerData.objects.all().delete()

def update_tickers_in_database():
    api_key = "c526e7cb-b641-49e4-81f6-a855a3de479a"
    ss = StockSymbol(api_key)

    symbol_list_us = ss.get_symbol_list(market="US", symbols_only=False)
    symbol_df = pd.DataFrame(symbol_list_us)
    entries = []
    for row in symbol_df.to_dict('records'):
        record = StockTickerData(symbol=row["symbol"], shortName=row["shortName"], longName=row["longName"],
                                 exchange=row["exchange"], market=row["market"], quoteType=row["quoteType"])
        entries.append(record)

    StockTickerData.objects.bulk_create(entries)