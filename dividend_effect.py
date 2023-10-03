import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def plot_dividends_effect(ticker):
    stock_data = yf.Ticker(ticker)
    historical_data = stock_data.history(period="max")
    
    # Filter data to include only dates between January 1, 2018, and December 31, 2022
    historical_data = historical_data[(historical_data.index >= "2020-07-01") & (historical_data.index <= "2023-09-30")]
    
    dividends = stock_data.dividends

    # Create DataFrame to store dividend events
    dividend_events = pd.DataFrame(index=historical_data.index)
    dividend_events["Dividend"] = dividends

    # Mark dividend events in the DataFrame
    dividend_events["Dividend_Event"] = dividend_events["Dividend"].notna().astype(int)

    # Merge dividend events with historical data
    historical_data = pd.merge(historical_data, dividend_events, how="left", left_index=True, right_index=True)

    # Create a new column for stock price without dividends
    historical_data["Close_No_Dividends"] = historical_data["Close"] + historical_data["Dividend"].fillna(0)

    # Plot the stock price with dividends
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot stock price with dividends
    ax.plot(historical_data.index, historical_data["Close"], label="Stock Price (with Dividends)", color="blue")

    # Plot stock price without dividends within a week before and after each dividend payment
    for date in historical_data[dividend_events["Dividend_Event"] == 1].index:
        start_date = date - pd.Timedelta(days=7)
        end_date = date + pd.Timedelta(days=7)
        dividend_period_data = historical_data.loc[start_date:end_date]
        historical_period_data = historical_data["Close"].loc[start_date:end_date]
        #ax.plot(historical_period_data.index, historical_period_data, label="Stock Price (with Dividends)", color="blue")
        ax.plot(dividend_period_data.index, dividend_period_data["Close_No_Dividends"], label=f"Stock Price (Dividends: {date.date()})", alpha=0.7)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    ax.tick_params(axis="y")
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.title(f"Stock Price with and without Dividends for {ticker} (2018-2022)")
    plt.tight_layout()
    plt.show()

# Replace 'FMG.AX' with any other ASX ticker symbol
plot_dividends_effect('FMG.AX')
