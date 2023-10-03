import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

start_time = time.time()

# List of ASX stock tickers to analyze
stock_symbols = ['TCL.AX', 'SCG.AX', 'TLS.AX', 'FMG.AX', 'CRN.AX']

all_asx_tickers = pd.read_csv('https://www.asx.com.au/asx/research/ASXListedCompanies.csv', header=1)
asx_tickers = all_asx_tickers[all_asx_tickers != 'Not Applic']
print(asx_tickers)
    
filtered_stocks = []
stock_symbols = []
min_assets = 1e9

period = 10

ignore_list = ['ABP.AX']
    
for _, row in asx_tickers.iterrows():
    stock_symbols.append(row['ASX code'] + '.AX')


def calculate_returns(data, interval):
    # Calculate the returns based on the interval
    if interval == '1H':
        return data['Close'].pct_change(periods=60) * 100
    elif interval == '1D':
        return data['Close'].pct_change(periods=390) * 100
    else:
        raise ValueError("Invalid interval. Supported intervals: '1H', '1D'")

def get_1min_data(stock_symbol):
    # Fetch data for the period with a 1-minute interval using multiple requests
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(days=period)

    data_1min = pd.DataFrame()
    while end_date > start_date:
        data = yf.download(stock_symbol, start=end_date - pd.DateOffset(days=7), end=end_date, interval='1m')
        data_1min = pd.concat([data_1min, data])
        end_date -= pd.DateOffset(days=1)

    data_1min = data_1min.dropna()
    return data_1min

def plot_returns_distribution(stock_symbols):
    # Plot the distributions
    fig, ax = plt.subplots(figsize=(10, 6))

    for stock_symbol in stock_symbols:
        if stock_symbol not in ignore_list:
            try:
                total_assets = yf.Ticker(stock_symbol).balance_sheet.loc['Total Assets'].tail(1).values[0]

                if total_assets > min_assets:
                    print(stock_symbol,total_assets)
                    # Fetch 1-minute data for the last 28 days
                    data_1min = get_1min_data(stock_symbol)

                    if data_1min.empty:
                        print(f"No valid 1-minute data available for {stock_symbol}")
                        continue

                    # Calculate returns for 1-minute interval
                    data_1min['1M_Return'] = calculate_returns(data_1min, '1D')

                    # Find and print the minimum and maximum 1-minute returns and the times they occurred
                    min_return_1min = data_1min['1M_Return'].min()
                    max_return_1min = data_1min['1M_Return'].max()
                    time_min_return_1min = data_1min['1M_Return'].idxmin()
                    time_max_return_1min = data_1min['1M_Return'].idxmax()

                    # Check if the distribution is skewed towards positive or negative returns
                    skewness = data_1min['1M_Return'].skew()
                    if skewness > 0.2:
                        skew_direction = "Positive"
                        print(f"{stock_symbol} Skewness: {skewness}, {skew_directino}")
                        print(f"{stock_symbol} Min 1-Minute Return: {min_return_1min:.2f}% at {time_min_return_1min}")
                        print(f"{stock_symbol} Max 1-Minute Return: {max_return_1min:.2f}% at {time_max_return_1min}")
                        ax.hist(data_1min['1M_Return'], bins=50, alpha=0.7, label=f"{stock_symbol} 1 Minute Returns (Last 28 days)")
                    elif skewness < 0:
                        skew_direction = "Negative"
                    else:
                        skew_direction = "Symmetrical"
                        
            except Exception as e:
                print(f"Error processing {stock_symbol}: {e}")

    end_time = time.time()  # Record the end time
    total_time = end_time - start_time  # Calculate the total runtime

    print(f"Total time taken: {total_time:.2f} seconds")
    
    ax.set_xlabel("Returns (%)")
    ax.set_ylabel("Frequency")
    ax.legend(loc='upper right')
    plt.title(f"Distribution of 1m Returns last 28 days")
    plt.tight_layout()
    plt.show()

# Plot the distributions for the selected ASX stocks
plot_returns_distribution(stock_symbols)
