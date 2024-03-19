#import libraries
import logging
import pandas as pd
from kiteconnect import KiteConnect

# For logging-in purpose 
logging.basicConfig(level=logging.DEBUG)

# Initialize Kite object with your API key
kite = KiteConnect(api_key="8a6f62gf3y0ei7o9")

# Set the access token directly (replace "your_access_token" with your actual access token)
kite.set_access_token("pFyqoyxe4PV19gVMRXTfr2I0cC2s4Cdm")

# Get instrument tokens for Reliance, ACC, and ITC
instruments = kite.ltp(['NSE:RELIANCE', 'NSE:ACC', 'NSE:ITC'])

# Extract instrument tokens
reliance_token = instruments['NSE:RELIANCE']['instrument_token']
acc_token = instruments['NSE:ACC']['instrument_token']
itc_token = instruments['NSE:ITC']['instrument_token']

# Fetch historical data for the last 30 days with 1-minute interval
reliance_data = kite.historical_data(reliance_token, "2024-02-18 09:15:00", "2024-03-18 15:30:00", "minute", continuous=False)
acc_data = kite.historical_data(acc_token, "2024-02-18 09:15:00", "2024-03-18 15:30:00", "minute", continuous=False)
itc_data = kite.historical_data(itc_token, "2024-02-18 09:15:00", "2024-03-18 15:30:00", "minute", continuous=False)

# Convert historical data to DataFrame
reliance_df = pd.DataFrame(reliance_data)
acc_df = pd.DataFrame(acc_data)
itc_df = pd.DataFrame(itc_data)

# Resample data to 8-minute candles
# T means minute in pandas
reliance_df_resampled = reliance_df.resample('8T', on='date').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).dropna()

acc_df_resampled = acc_df.resample('8T', on='date').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).dropna()

itc_df_resampled = itc_df.resample('8T', on='date').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).dropna()

# Calculate HMA for 8-period 
# We use .ewm Exponetial weighted function useful for observing recent observation
def calculate_hma(df, period=8):
    df['hma'] = df['close'].ewm(span=period).mean()
    return df

# Calculate SMA for 8-period
def calculate_sma(df, period=8):
    df['sma'] = df['close'].rolling(window=period).mean()
    return df

# Apply functions to each DataFrame
reliance_df_resampled = calculate_hma(reliance_df_resampled)
reliance_df_resampled = calculate_sma(reliance_df_resampled)

acc_df_resampled = calculate_hma(acc_df_resampled)
acc_df_resampled = calculate_sma(acc_df_resampled)

itc_df_resampled = calculate_hma(itc_df_resampled)
itc_df_resampled = calculate_sma(itc_df_resampled)

# Define functions for signals 
# If FM signal is True or False
def hma_signal(df):
    df['hma_signal'] = (df['hma'].shift(1) < 70) & (df['hma'] > 70)
    return df

def sma_signal(df):
    df['sma_signal'] = (df['sma'].shift(1) < df['close'].shift(1)) & (df['sma'] > df['close'])
    return df

# Apply signal functions to each DataFrame
reliance_df_resampled = hma_signal(reliance_df_resampled)
reliance_df_resampled = sma_signal(reliance_df_resampled)

acc_df_resampled = hma_signal(acc_df_resampled)
acc_df_resampled = sma_signal(acc_df_resampled)

itc_df_resampled = hma_signal(itc_df_resampled)
itc_df_resampled = sma_signal(itc_df_resampled)

# Export to CSV
reliance_df_resampled.to_csv('reliance_data.csv')
acc_df_resampled.to_csv('acc_data.csv')
itc_df_resampled.to_csv('itc_data.csv')

reliance_df = pd.read_csv('reliance_data.csv', index_col=0)
acc_df = pd.read_csv('acc_data.csv', index_col=0)
itc_df = pd.read_csv('itc_data.csv', index_col=0)

# Display first few rows of each DataFrame
print("Reliance Data:")
print(reliance_df.head())
print("\nACC Data:")
print(acc_df.head())
print("\nITC Data:")
print(itc_df.head())