import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

purchase_prices = {}
#to buy
#purchase_prices['TPG.AX'] = 5.1 #
#purchase_prices['ANZ.AX'] = 23 #
#purchase_prices['WBC.AX'] = 18 #
#purchase_prices['CBA.AX'] = 98 #4%!
#purchase_prices['STO.AX'] = 7.5 #4.19%!
#purchase_prices['QBE.AX'] = 15.2 #2.46%
#purchase_prices['AFI.AX'] = 7.15 #3.47%
#purchase_prices['EZL.AX'] =  1.02
#purchase_prices['KOV.AX'] =  8.0
#purchase_prices['GNE.AX'] =  2.1
#purchase_prices['ALX.AX'] =  5.85 #23 Sep!
#purchase_prices['VSL.AX'] =  7.5 #27 Sep

#purchase_prices['HVN.AX'] =  3.6 #13 Oct!
#purchase_prices['WAM.AX'] =  1.63 #17 Oct
purchase_prices['NHC.AX'] =  6.0 #5.6 #23 Oct!
#purchase_prices['BOQ.AX'] =  5.6 #Oct!



#purchase_prices['STW.AX'] = 66 #3.47%
#purchase_prices['SLF.AX'] = 66 #3.47%
#purchase_prices['SFY.AX'] = 65 #3.47%

#in money
#purchase_prices['AGL.AX'] = 16.8
purchase_prices['FMG.AX'] = 21.68 #10,016: 425 old 23.52||| 980.59: 45 new 21.68
#purchase_prices['ASH.AX'] =  0.68 #957
#purchase_prices['TLS.AX'] =  4.12 # 2884 4.12
#purchase_prices['TCL.AX'] =  12.6 #Dec 2,857.6 226 TCL at 1260

stock_symbols = [key for key in purchase_prices.keys()]

daysOffset = 28

def calculate_returns(data, interval):
    # Calculate the returns based on the interval
    if interval == '1H':
        return data['Close'].pct_change(periods=60) * 100
    elif interval == '1D':
        return data['Close'].pct_change(periods=390) * 100
    else:
        raise ValueError("Invalid interval. Supported intervals: '1H', '1D'")

def get_1min_data(stock_symbol):
    # Fetch data for the last 28 days with a 1-minute interval
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(days=daysOffset)

    data_1min = pd.DataFrame()
    while end_date > start_date:
        data = yf.download(stock_symbol, start=end_date - pd.DateOffset(days=7), end=end_date, interval='1m')
        data_1min = pd.concat([data_1min, data])
        end_date -= pd.DateOffset(days=7)

    return data_1min

def plot_returns_distribution(stock_symbols):
    # Plot the distributions
    fig, ax = plt.subplots(figsize=(10, 6))

    for stock_symbol in stock_symbols:
        print(stock_symbol)
##        # Fetch 1-minute data for the last 28 days
##        data_1min = get_1min_data(stock_symbol)
##
##        # Filter out rows with NaN values
##        data_1min = data_1min.dropna()
##
##        if data_1min.empty:
##            print(f"No valid 1-minute data available for {stock_symbol}")
##            return

        # Fetch data for daysOffset with a 1-day interval
        end_date_1d = pd.Timestamp.now()
        start_date_1d = end_date_1d - pd.DateOffset(days=daysOffset)

        data_1d = yf.download(stock_symbol, start=start_date_1d, end=end_date_1d, interval='1h')

        # Filter out rows with NaN values
        data_1d = data_1d.dropna()

        if data_1d.empty:
            print(f"No valid 1-day data available for {stock_symbol}")
            return

        # Calculate returns for different intervals
        #data_1min['1M_Return'] = calculate_returns(data_1min, '1D')
        data_1d['1H_Return'] = calculate_returns(data_1d, '1H')

        #ax.hist(data_1min['1M_Return'], bins=50, alpha=0.7, label=f"{stock_symbol} 1 Minute Returns for the last {daysOffset} days")
        ax.hist(data_1d['1H_Return'], bins=50, alpha=0.7, label=f'{stock_symbol} 1 Hour Returns for the last {daysOffset} days')

    # Limit x-axis to 3 standard deviations from the mean
    #mean_1min = np.mean(data_1min['1M_Return'])
    #std_1min = np.std(data_1min['1M_Return'])
    #ax.set_xlim([mean_1min - 3 * std_1min, mean_1min + 3 * std_1min])

    ax.set_xlabel("Returns (%)")
    ax.set_ylabel("Frequency")
    ax.legend(loc='upper right')
    plt.title(f"Distribution of 1m Returns last 28 days")
    plt.tight_layout()
    plt.show()

# Replace 'FMG.AX' with any other ASX ticker symbol
plot_returns_distribution(stock_symbols)
