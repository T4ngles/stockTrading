import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy
import datetime
import time

# Define the ASX stock symbols and their respective normalization prices
#stock_symbols = ["AFI.AX", "CRN.AX", "FMG.AX", "MIR.AX", "NEC.AX", "TLS.AX"] #change to dictionary with stock symbols and purchase price
#normalization_prices = [7.0, 1.72, 23.52, 2.875, 2.01, 4.2]

#stock_symbols = ['CBA.AX', 'FMG.AX', 'GNE.AX', 'VSL.AX', 'TLS.AX', 'HVN.AX', 'ASH.AX', 'JCS.AX', 'AFI.AX']

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

purchase_prices['MFF.AX'] =  2.98 #6 Oct!
purchase_prices['HVN.AX'] =  3.6 #13 Oct!
purchase_prices['WAM.AX'] =  1.63 #17 Oct
purchase_prices['NHC.AX'] =  6.0 #5.6 #23 Oct!
#purchase_prices['BOQ.AX'] =  5.6 #Oct!



#purchase_prices['STW.AX'] = 66 #3.47%
#purchase_prices['SLF.AX'] = 66 #3.47%
#purchase_prices['SFY.AX'] = 65 #3.47%

#in money
#purchase_prices['AGL.AX'] = 16.8
purchase_prices['FMG.AX'] = 21.68 #10,016: 425 old 23.52||| 980.59: 45 new 21.68
#purchase_prices['ASH.AX'] =  0.68 #957
purchase_prices['TLS.AX'] =  4.12 # 2884 4.12
purchase_prices['TCL.AX'] =  12.6 #Dec 2,857.6 226 TCL at 1260

stock_symbols = [key for key in purchase_prices.keys()]

in_money = ['FMG.AX', 'TLS.AX', 'ASH.AX', 'TCL.AX']

# Trading hours in 24-hour format (10 am to 4 pm)
now = datetime.datetime.now()
trading_start = datetime.time(10, 0)
trading_end = datetime.time(16, 0)

fig = plt.figure()

def get_normalized_prices(stock_symbols):
    ani = animation.FuncAnimation(fig,animate,interval=60000,cache_frame_data=False)
    plt.show()    

def animate(i):
    # Fetch historical data for the last 72 hours
    historical_data = yf.download(stock_symbols, period="1d", interval="1m")["Close"]
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Normalize prices to the given normalization prices
    normalization_prices = [purchase_prices[x] for x in list(historical_data)] #account for order that yf downloads data

    normalized_data = historical_data / normalization_prices
    
    for stock_symbol in stock_symbols:
        print(stock_symbol,":",round(historical_data[stock_symbol][-1],2)," purchase:",purchase_prices[stock_symbol]," norm:",round(normalized_data[stock_symbol][-1],2))
    plt.cla()

    # Plot the normalized prices
    for stock_symbol in stock_symbols:
        #range(normalized_data.index.size) gives only the count of the index instead of the time

        #get rid of nans if no trades in the past minutes
        i = 1
        while numpy.isnan(historical_data[stock_symbol][-i]):
            i += 1
            
        if stock_symbol in in_money:
            plt.plot(range(normalized_data.index.size),
                     normalized_data[stock_symbol],
                     label=f"{stock_symbol} (buy:${purchase_prices[stock_symbol]:.2f})(cur:${historical_data[stock_symbol][-i]:.2f})",
                     marker='x')
        else:
            plt.plot(range(normalized_data.index.size),
                     normalized_data[stock_symbol],
                     label=f"{stock_symbol} (buy:${purchase_prices[stock_symbol]:.2f})(cur:${historical_data[stock_symbol][-i]:.2f})",
                     marker='o')

        plt.xlabel("Time")
        plt.ylabel("Normalized Price")
        plt.title(f"Normalized Prices for ASX Stocks(As of {current_time})")
        plt.legend(loc='upper left')
        plt.grid()
    plt.axhline(y=1, color='black', linestyle='--', label='Purhcase')    
    plt.axhline(y=1.01, color='red', linestyle='--', label='Target1')
    plt.axhline(y=1.02, color='green', linestyle='--', label='Target2')
    plt.yticks(numpy.arange(0.95, 1.1, 0.01))
        

    
if __name__ == "__main__":
    get_normalized_prices(stock_symbols)
