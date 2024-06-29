import numpy as np
import pandas as pd
import talib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Generate synthetic bond price data
def generate_bond_data(start_date, end_date, initial_price=100):
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    prices = initial_price + np.cumsum(np.random.normal(0, 0.1, len(date_range)))
    return pd.DataFrame({'Date': date_range, 'Price': prices}).set_index('Date')

# Calculate TA-Lib indicators
def calculate_indicators(df):
    df['RSI'] = talib.RSI(df['Price'])
    df['SMA_20'] = talib.SMA(df['Price'], timeperiod=20)
    df['SMA_50'] = talib.SMA(df['Price'], timeperiod=50)
    df['MACD'], df['MACD_Signal'], df['MACD_Hist'] = talib.MACD(df['Price'])
    df['Upper'], df['Middle'], df['Lower'] = talib.BBANDS(df['Price'], timeperiod=20)
    return df

# Generate trading signals
def generate_signals(df):
    df['Signal'] = 0  # 0: Hold, 1: Buy, -1: Sell
    
    # RSI signals
    df.loc[df['RSI'] < 30, 'Signal'] = 1
    df.loc[df['RSI'] > 70, 'Signal'] = -1
    
    # Moving Average Crossover
    df.loc[(df['SMA_20'] > df['SMA_50']) & (df['SMA_20'].shift(1) <= df['SMA_50'].shift(1)), 'Signal'] = 1
    df.loc[(df['SMA_20'] < df['SMA_50']) & (df['SMA_20'].shift(1) >= df['SMA_50'].shift(1)), 'Signal'] = -1
    
    # MACD signals
    df.loc[(df['MACD'] > df['MACD_Signal']) & (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1)), 'Signal'] = 1
    df.loc[(df['MACD'] < df['MACD_Signal']) & (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1)), 'Signal'] = -1
    
    # Bollinger Bands signals
    df.loc[df['Price'] < df['Lower'], 'Signal'] = 1
    df.loc[df['Price'] > df['Upper'], 'Signal'] = -1
    
    return df

# Backtest strategy
def backtest_strategy(df):
    df['Position'] = df['Signal'].shift(1)
    df['Returns'] = df['Price'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Returns']
    
    cumulative_returns = (1 + df['Strategy_Returns']).cumprod()
    total_return = cumulative_returns.iloc[-1] - 1
    sharpe_ratio = np.sqrt(252) * df['Strategy_Returns'].mean() / df['Strategy_Returns'].std()
    
    return cumulative_returns, total_return, sharpe_ratio

# Visualize results
def plot_results(df, cumulative_returns):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16))
    
    # Plot 1: Price and Moving Averages
    ax1.plot(df.index, df['Price'], label='Bond Price')
    ax1.plot(df.index, df['SMA_20'], label='SMA 20')
    ax1.plot(df.index, df['SMA_50'], label='SMA 50')
    ax1.fill_between(df.index, df['Upper'], df['Lower'], alpha=0.2, label='Bollinger Bands')
    ax1.scatter(df.index[df['Signal'] == 1], df['Price'][df['Signal'] == 1], marker='^', color='g', label='Buy Signal')
    ax1.scatter(df.index[df['Signal'] == -1], df['Price'][df['Signal'] == -1], marker='v', color='r', label='Sell Signal')
    ax1.set_title('Bond Price with Signals')
    ax1.legend()
    
    # Plot 2: RSI
    ax2.plot(df.index, df['RSI'], label='RSI')
    ax2.axhline(y=30, color='g', linestyle='--')
    ax2.axhline(y=70, color='r', linestyle='--')
    ax2.set_title('Relative Strength Index (RSI)')
    ax2.legend()
    
    # Plot 3: Cumulative Returns
    ax3.plot(cumulative_returns.index, cumulative_returns, label='Strategy Returns')
    ax3.set_title('Cumulative Returns of Trading Strategy')
    ax3.legend()
    
    plt.tight_layout()
    plt.show()

# Main function
def main():
    # Generate synthetic bond data
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 1, 1)
    df = generate_bond_data(start_date, end_date)
    
    # Calculate indicators
    df = calculate_indicators(df)
    
    # Generate signals
    df = generate_signals(df)
    
    # Backtest strategy
    cumulative_returns, total_return, sharpe_ratio = backtest_strategy(df)
    
    # Print results
    print(f"Total Return: {total_return:.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    
    # Visualize results
    plot_results(df, cumulative_returns)

if __name__ == "__main__":
    main()