import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import hashlib
from matplotlib import colormaps
from matplotlib.colors import ListedColormap
import numpy as np

# Define the ASX stock symbols for the previous 20 companies
#stock_symbols = ["AFI.AX", "TLS.AX", "CBA.AX", "WBC.AX", "NAB.AX", "ANZ.AX", "BHP.AX", "RIO.AX", "WOW.AX", "WDS.AX", "AGL.AX", "SUN.AX", "MQG.AX", "TCL.AX", "APA.AX", "FMG.AX", "NEC.AX"]
#stock_symbols = ["AFI.AX", "CBA.AX", "WBC.AX", "NAB.AX", "ANZ.AX", "SUN.AX", "MQG.AX"]
#stock_symbols = ["TLS.AX", "BHP.AX", "WDS.AX", "AGL.AX", "TCL.AX", "APA.AX", "FMG.AX", "NEC.AX"]
#stock_symbols = ['CBA.AX', 'WBC.AX', 'ANZ.AX', 'NAB.AX', 'MQG.AX', 'TCL.AX', 'SCG.AX', 'TLS.AX', 'APA.AX', 'QBE.AX', 'ORG.AX', 'DOW.AX', 'STO.AX']
#stock_symbols = ['WBC.AX', 'ANZ.AX', 'NAB.AX', 'SUN.AX', 'CBA.AX', 'MQG.AX', 'FMG.AX', 'TLS.AX', 'BHP.AX', 'TCL.AX', 'AGL.AX', 'APA.AX', 'NEC.AX', 'WDS.AX', 'SCG.AX', 'QBE.AX', 'ORG.AX', 'DOW.AX', 'STO.AX']

#August Divs
stock_symbols = ['SUN.AX', 'SCG.AX', 'CBA.AX', 'QBE.AX', 'STO.AX', 'TLS.AX', 'DOW.AX']

#pot_comps
stock_symbols = ['AGL.AX','AMP.AX','ATM.AX','ANZ.AX','BOQ.AX','BEN.AX','BFL.AX','DXS.AX','FMG.AX','GPT.AX','IAG.AX','LFG.AX','MGR.AX','NAB.AX','ORG.AX','QBE.AX','STO.AX','SCG.AX','SGP.AX','SUN.AX','TAH.AX','TLS.AX','URW.AX','VCX.AX','WBC.AX','WOR.AX','YAL.AX']

print(len(stock_symbols), " stocks:",stock_symbols)

start_date = datetime.datetime(2020, 1, 1, tzinfo=None)
start_date20 = datetime.datetime(2020, 1, 1, tzinfo=None)
end_date = datetime.datetime(2023, 7, 1, tzinfo=None)

def hash_name(name):
    # Use SHA256 hashing to generate a unique numeric value for each stock name
    sha256 = hashlib.sha256(name.encode()).hexdigest()
    return int(sha256, 16)  # Convert the hexadecimal hash to an integer

def normalize_stock_prices(stock_data):
    # Get balance sheet data for the stock
    balance_sheet = stock_data.balance_sheet

    # Extract the 'Total Assets' from the balance sheet
    total_assets = balance_sheet.loc['Total Assets']/1000000000

    # Remove timezone information from the index
    total_assets.index = total_assets.index.tz_localize(None)
    #print(total_assets)

    # Normalize stock prices by dividing them by the total assets
    
    stock_prices = stock_data.history(start=start_date, end=end_date)['Close']
    stock_prices.index = stock_prices.index.tz_localize(None)
    normalized_prices = stock_prices / total_assets
    #print(normalized_prices)
    return normalized_prices

def plot_dividend_yields_and_normalized_prices(stock_symbols):
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

    # Get a colormap to assign colors based on the hash of ticker symbols
    colormap = colormaps.get_cmap('tab20')

    for i, stock_symbol in enumerate(stock_symbols):
        # Fetch historical dividend data for the stock
        stock_data = yf.Ticker(stock_symbol)
        dividend_data = stock_data.dividends
        
        # Filter out dividend data for the years
        dividend_data.index = dividend_data.index.tz_localize(None)
        dividend_data = dividend_data[start_date:end_date]

        # Remove timezone information from the index
        dividend_data.index = dividend_data.index.tz_localize(None)

        # Calculate the dividend yield for each dividend payment
        historical_data = stock_data.history(start=start_date, end=end_date)['Close']
        historical_data.index = historical_data.index.tz_localize(None)
        dividend_yield = dividend_data / historical_data

        color = colormap(i)

        mask = np.isfinite(dividend_yield)
        
        # Plot the dividend yields for the stock with the assigned color in the first subplot
        ax1.plot(dividend_yield.index[mask], dividend_yield[mask], label=stock_data.info["longName"], color=color, marker='o')

        # Normalize stock prices for the stock
        normalized_prices = normalize_stock_prices(stock_data)

        print('div: {0:.2f}'.format(dividend_yield.mean()*100),'norm: {0:.2f}'.format(normalized_prices.mean()),stock_symbol, stock_data.info["longName"],'ind: {0:.2f}'.format(dividend_yield.mean()*100/normalized_prices.mean()))

        # Plot the normalized stock prices for the stock with the assigned color in the second subplot
        ax2.plot(normalized_prices.index, normalized_prices, label=stock_data.info["longName"], color=color,  marker='o')

    ax1.set_ylabel("Dividend Yield")
    ax1.set_title("Dividend Yields for ASX Stocks (2014-2020)")
    ax1.legend(loc='upper left')
    ax1.grid()

    ax2.set_ylabel("Normalized Stock Price")
    ax2.set_title("Normalized Stock Prices for ASX Stocks (2014-2020)")
    ax2.legend(loc='upper left')
    ax2.grid()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_dividend_yields_and_normalized_prices(stock_symbols)
