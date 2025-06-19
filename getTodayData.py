from stockKey import key, stocks
from twelvedata import TDClient
import pandas as pd

td = TDClient(apikey=key)

# Fetch data for each stock
for stock in stocks:
    try:
        print(f"Fetching data for {stock}...")
        
        price_data = td.price(symbol=stock).as_json()
        
        print(f"✅ Current price for {stock}:")
        print(f"Price: {price_data['price']}")
        
    except Exception as e:
        print(f"❌ Failed for {stock}: {e}")