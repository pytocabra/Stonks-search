import pandas as pd
from stocksymbol import StockSymbol

api_key = "c526e7cb-b641-49e4-81f6-a855a3de479a"
ss = StockSymbol(api_key)

symbol_list_us = ss.get_symbol_list(market="US", symbols_only=False)
symbol_df = pd.DataFrame(symbol_list_us)



print(symbol_df)