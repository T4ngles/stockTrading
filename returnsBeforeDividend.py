import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the list of stock symbols
stock_symbols = ['NHC.AX']

# Define the start date for data retrieval
start_date = '2021-01-01'

# Initialize variables to track maximum returns
max_return = 0
max_return_stock = None
max_return_date = None

weeklyReturn = {}

# Loop through each stock symbol
for symbol in stock_symbols:
    # Create a Ticker object for the stock
    stock = yf.Ticker(symbol)

    # Get dividend data for the stock
    dividends = stock.dividends

    # Filter dividends for dates on or after the start date
    dividends = dividends[dividends.index >= start_date]

    # Loop through ex-dividend dates and calculate returns
    for ex_dividend_date, dividend_amount in dividends.items():
        # Calculate the start and end dates for the week surrounding the ex-dividend date
        start_week = ex_dividend_date - timedelta(days=21)
        end_week = ex_dividend_date

        # Fetch historical data for the stock for that week
        stock_data = stock.history(period="1d", start=start_week, end=end_week)

        if stock_data.empty:
            continue
        
        # Calculate weekly returns as (closing price - opening price) / opening price
        stock_data['Weekly_Return'] = (stock_data['Close'] - stock_data['Open']) / stock_data['Open']

        #maxWeek = 0        
        
        for i in range(len(stock_data['Close'])):
            weeklyReturn[i] = (stock_data['Close'].iloc[len(stock_data['Close'])-1] - stock_data['Close'].iloc[i]) / stock_data['Close'].iloc[i]
            print(f"{symbol}:{i} - {weeklyReturn[i]*100:.2f}% {stock_data['Close'].iloc[i]:.2f}")
        # Find the maximum weekly return and its corresponding date
        max_weekly_return = stock_data['Weekly_Return'].max()
        max_weekly_return_date = stock_data['Weekly_Return'].idxmax()

        #print(f"{symbol}: {max_weekly_return * 100:.2f}% on {max_weekly_return_date.strftime('%Y-%m-%d')}")

        # Check if this return is greater than the current maximum return
        if max_weekly_return > max_return:
            max_return = max_weekly_return
            max_return_stock = symbol
            max_return_date = max_weekly_return_date

# Print the stock with the maximum weekly return and the corresponding date
print(f"Stock with maximum weekly return: {max_return_stock}")
print(f"Maximum weekly return: {max_return * 100:.2f}%")
print(f"Date of maximum weekly return: {max_return_date.strftime('%Y-%m-%d')}")
