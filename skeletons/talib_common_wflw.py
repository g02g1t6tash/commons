import numpy as np
import pandas as pd
import talib
from pandas_datareader import data as pdr

# 1. Fetch financial data
def get_stock_data(symbol, start_date, end_date):
    df = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
    return df

# 2. Prepare data for TALib
def prepare_data(df):
    close = df['Close'].values
    high = df['High'].values
    low = df['Low'].values
    volume = df['Volume'].values
    return close, high, low, volume

# 3. Calculate technical indicators
def calculate_indicators(close, high, low, volume):
    # Simple Moving Average
    sma = talib.SMA(close, timeperiod=20)
    
    # Relative Strength Index
    rsi = talib.RSI(close, timeperiod=14)
    
    # Moving Average Convergence Divergence
    macd, macd_signal, _ = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    
    # Bollinger Bands
    upper, middle, lower = talib.BBANDS(close, timeperiod=20)
    
    # On-Balance Volume
    obv = talib.OBV(close, volume)
    
    return sma, rsi, macd, macd_signal, upper, middle, lower, obv

# 4. Main workflow
def main():
    # Set parameters
    symbol = 'AAPL'
    start_date = '2022-01-01'
    end_date = '2023-01-01'
    
    # Get data
    df = get_stock_data(symbol, start_date, end_date)
    
    # Prepare data
    close, high, low, volume = prepare_data(df)
    
    # Calculate indicators
    sma, rsi, macd, macd_signal, upper, middle, lower, obv = calculate_indicators(close, high, low, volume)
    
    # Add indicators to dataframe
    df['SMA'] = sma
    df['RSI'] = rsi
    df['MACD'] = macd
    df['MACD_Signal'] = macd_signal
    df['BB_Upper'] = upper
    df['BB_Middle'] = middle
    df['BB_Lower'] = lower
    df['OBV'] = obv
    
    # Print results
    print(df.tail())

if __name__ == "__main__":
    main()