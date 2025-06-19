from stockKey import key, stocks
from twelvedata import TDClient
import pandas as pd

td = TDClient(apikey=key)

# Fetch data for each stock
for symbol in stocks:
    try:
        print(f"Fetching data for {symbol}...")
        
        data = td.time_series(
            symbol=symbol,
            interval="1day",
            outputsize=1260,  # 5 years = ~1260 trading days
            timezone="America/New_York",
        ).as_pandas()
        
        # Save to CSV
        data.to_csv(f"data/{symbol}_5y_data.csv")
        print(f"✅ Saved {symbol}_5y_data.csv")
    
    except Exception as e:
        print(f"❌ Failed for {symbol}: {e}")