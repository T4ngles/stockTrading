import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy
import datetime
import time

low_cutoff_ratio = 0.95
high_cutoff_ratio = 1.05

class Stock_Trace:
    _stock_dict = {}
    
    def __init__(self, ticker, price, in_money, ex_date=None, div=None):
        self.ticker = ticker
        self.price = price        
        self.div = div
        self.in_money = in_money
        self.ex_date = ex_date
        if self.ex_date:
            self.ex_date = datetime.datetime.strptime(self.ex_date, '%d/%m/%Y')
        Stock_Trace._stock_dict[self.ticker] = self
        
    def div_return(self):
        return self.div/self.price
    
    def days_left(self):
        if self.ex_date:            
            today = datetime.datetime.today()            
            if self.ex_date > today:
                return (self.ex_date - today).days
            else:
                return None
        else:
            return None            
        
Stock_Trace('TPG.AX', 5.1, False)
Stock_Trace('CBA.AX', 95.0, False)
Stock_Trace('YAL.AX', 4.88, False)
Stock_Trace('STO.AX', 7.2, False)
Stock_Trace('QBE.AX', 15.2, False)
Stock_Trace('AFI.AX', 7.15, False)
Stock_Trace('EZL.AX', 1.02, False)
Stock_Trace('KOV.AX', 8.0, False)
Stock_Trace('GNE.AX', 2.1, False)
Stock_Trace('ALX.AX', 5.85, False)
Stock_Trace('VSL.AX', 7.5, False)
Stock_Trace('NEC.AX', 1.95, False)
Stock_Trace('MFF.AX', 2.98, False)
Stock_Trace('HVN.AX', 3.6, False)
Stock_Trace('FGX.AX', 1.07, False)
Stock_Trace('UOS.AX', 0.52, False)
Stock_Trace('HZN.AX', 0.15, False)
Stock_Trace('WAM.AX', 1.50, False)
Stock_Trace('NCM.AX', 22.5, False)
Stock_Trace('KSC.AX', 2.0, False)
Stock_Trace('STW.AX', 66.0, False)
Stock_Trace('SLF.AX', 66.0, False)
Stock_Trace('SFY.AX', 65.0, False)

Stock_Trace('NHC.AX', 6.18, False, "23/10/2023", 0.3)
Stock_Trace('ASG.AX', 2.3, False, "31/10/2023", 0.1)
Stock_Trace('BOQ.AX', 5.35, False, "26/10/2023", 0.21)
Stock_Trace('CVL.AX', 0.88, False, "29/11/2023", 0.03)
Stock_Trace('ACF.AX', 0.80, False, "26/10/2023", 0.027)

#in money
Stock_Trace('AGL.AX', 16.8, True)
Stock_Trace('FMG.AX', 23.52, True)
Stock_Trace('ASH.AX', 0.68, True)
Stock_Trace('TLS.AX', 4.12, True)
Stock_Trace('TCL.AX', 12.8, True)
Stock_Trace('WLE.AX', 1.47, True, "17/10/2023", 0.045)
Stock_Trace('ANZ.AX', 27.06, True)
Stock_Trace('WBC.AX', 23.05, True)

#todo: incorporate ex div dates into dictionary so stocks come up on ticker within +-1month of current date

stock_symbols = [key for key in Stock_Trace._stock_dict.keys()]

# Trading hours in 24-hour format (10 am to 4 pm)
now = datetime.datetime.now()
trading_start = datetime.time(10, 0)
trading_end = datetime.time(16, 0)

fig = plt.figure()

index_error = []

def get_normalized_prices(stock_symbols):
    ani = animation.FuncAnimation(fig,animate,interval=30000,cache_frame_data=False)
    plt.show()    

def animate(i):
    # Fetch historical data for the last 72 hours
    historical_data = yf.download(stock_symbols, period="2d", interval="1m")["Close"]
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Normalize prices to the given normalization prices
    normalization_prices = [ Stock_Trace._stock_dict[x].price for x in list(historical_data)] #account for order that yf downloads data

    normalized_data = historical_data / normalization_prices
    
    for stock_symbol in stock_symbols:
        print(stock_symbol,":",round(historical_data[stock_symbol][-1],2)," purchase:", Stock_Trace._stock_dict[stock_symbol].price," norm:",round(normalized_data[stock_symbol][-1],2))
    plt.cla()

    # Plot the normalized prices
    for stock_symbol in stock_symbols:

        if Stock_Trace._stock_dict[stock_symbol].days_left() or Stock_Trace._stock_dict[stock_symbol].in_money == True:
            #range(normalized_data.index.size) gives only the count of the index instead of the time       
            i = 1

            try:
                while numpy.isnan(historical_data[stock_symbol][-i]):  #get rid of nans if no trades in the past minutes
                    i += 1
            except IndexError:
                print(f"Index Error with {stock_symbol}")
                i = -1 * len(historical_data[stock_symbol])
                pass
            
            normalised_price = historical_data[stock_symbol][-i]/Stock_Trace._stock_dict[stock_symbol].price
            buy_price = Stock_Trace._stock_dict[stock_symbol].price
            current_price = historical_data[stock_symbol][-i]
            days_left = Stock_Trace._stock_dict[stock_symbol].days_left()
            
            if Stock_Trace._stock_dict[stock_symbol].div:
                div_yield = Stock_Trace._stock_dict[stock_symbol].div/current_price*100
            else:
                div_yield = 0
            
            if normalised_price > low_cutoff_ratio and normalised_price < high_cutoff_ratio:
                
                if Stock_Trace._stock_dict[stock_symbol].in_money:
                    plt.plot(range(normalized_data.index.size),
                             normalized_data[stock_symbol],
                             label=f"{stock_symbol[0:3]} \${buy_price:.2f}({current_price:.2f}) div: {div_yield:.2f}% ex:{days_left} ",
                             marker='x')
                else:
                    plt.plot(range(normalized_data.index.size),
                             normalized_data[stock_symbol],
                             label=f"{stock_symbol[0:3]} \${buy_price:.2f}({current_price:.2f}) div: {div_yield:.2f}% ex:{days_left} ",
                             marker='o')

                plt.xlabel("Time")
                plt.ylabel("Normalized Price")
                plt.title(f"Normalized Prices for ASX Stocks(As of {current_time})")
                plt.legend(loc='upper left')
                plt.grid()
    plt.axhline(y=1, color='black', linestyle='--', label='Purhcase')    
    plt.axhline(y=1.01, color='red', linestyle='--', label='Target1')
    plt.axhline(y=1.02, color='green', linestyle='--', label='Target2')
    plt.yticks(numpy.arange(low_cutoff_ratio, high_cutoff_ratio, 0.01))
        

    
if __name__ == "__main__":
    get_normalized_prices(stock_symbols)
