# From: https://algotrading101.com/learn/coinbase-pro-api-guid
# Use python 3.9

import cbpro
import requests
import pandas as pd
import pprint


c = cbpro.PublicClient()

# current ICP-USD
ticker = requests.get('https://api.pro.coinbase.com/products/ICP-USD/ticker').json()
print("Current price of ICP-USD:")
pprint.pprint(ticker)

# historical data
historical = pd.DataFrame(c.get_product_historic_rates(product_id='ICP-USD'))
historical.columns= ["Date","Open","High","Low","Close","Volume"]
historical['Date'] = pd.to_datetime(historical['Date'], unit='s')
historical.set_index('Date', inplace=True)
historical.sort_values(by='Date', ascending=True, inplace=True)
print("Historical price of ICP-USD:")
pprint.pprint(historical)

# data at certain dates
# Function to get historical prices for a specific date
def get_historical_prices(date):
    # Convert date to pandas datetime
    start_date = pd.to_datetime(date)
    end_date = start_date + pd.Timedelta(days=1)  # Adding one day to ensure the day is fully covered

    # Granularity - 86400 seconds (1 day) to get daily data
    historical_data = c.get_product_historic_rates('ICP-USD', 
                                                   start=start_date.isoformat(), 
                                                   end=end_date.isoformat(), 
                                                   granularity=86400)
    
    if historical_data and isinstance(historical_data, list):
        # Create DataFrame
        df = pd.DataFrame(historical_data, columns=["Time", "Low", "High", "Open", "Close", "Volume"])
        df['Date'] = pd.to_datetime(df['Time'], unit='s')
        df.set_index('Date', inplace=True)
        df.sort_index(ascending=True, inplace=True)
        return df
    else:
        print(f"No data returned for {date}")
        return None

# List of dates to check
dates = [
    "2023-01-07", "2023-01-15", "2023-01-28", "2023-02-04", 
    "2023-12-02", "2023-12-10", "2023-12-16", "2023-12-23",
]
# Fetch and print historical prices for each date
for date in dates:
    df = get_historical_prices(date)
    if df is not None:
        print(f"ICP-USD prices on {date}:")
        print(df[['Open', 'High', 'Low', 'Close', 'Volume']])

print("Now just the Low price at exactly those dates. for copy/paste in a spreadsheet:")
for date in dates:
    df = get_historical_prices(date)
    if df is not None:
        print(df.loc[date]["Low"])