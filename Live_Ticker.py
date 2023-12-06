'''


'''
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy
import datetime
import time
import os

#External Libs
import yfinance as yf

#Internal Libs
import scrapers.int_Inv_Scraper

low_cutoff_ratio = 0.95
high_cutoff_ratio = 1.1

class Stock_Trace:
    _stockDict = {}

    #getters and setters to allow access to class dictionary assignment
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def __init__(self, ticker: str, price: float, in_money: bool = False, ex_date: str = None, div: float = None):
        self.ticker = ticker
        self.price = price        
        self.div = div
        self.in_money = in_money
        self.ex_date = ex_date
        if self.ex_date:
            self.ex_date = datetime.datetime.strptime(self.ex_date, '%d/%m/%Y')

        if self.ticker in Stock_Trace._stockDict.keys():
            if input(f"Do you want to overwrite stored StockTrace for {self.ticker} with a calculated price:{Stock_Trace._stockDict[self.ticker].price} with the manual price:{price} y/n") == "y":
                print(f"overwritten with {price}")
                Stock_Trace._stockDict[ticker]["price"] = price
                Stock_Trace._stockDict[ticker]["in_money"] = in_money
            else:
                pass
        else:
            print(f"{ticker} added to stock traces at target price of {price}")
            Stock_Trace._stockDict[self.ticker] = self

    #create instance from a dictionary. Intent from scraping sources
    @classmethod
    def _fromDict(cls, extStockDict):
        for k,v in extStockDict.items():
            cls(v["ticker"], v["price"], v["in_money"], v["ex_date"], v["div"])
        
    def div_return(self) -> float:
        return self.div/self.price
    
    def days_left(self) -> int:
        if self.ex_date:            
            today = datetime.datetime.today()            
            if self.ex_date > today:
                return (self.ex_date - today).days
            else:
                return None
        else:
            return None            
        
Stock_Trace._fromDict(scrapers.int_Inv_Scraper.generateStockData())

#Manual
Stock_Trace('ELD.AX', 7.0, False)

#always trading
Stock_Trace('NEC.AX', 1.85, False)
Stock_Trace('NHC.AX', 4.5, False, "23/10/2023", 0.3)
Stock_Trace('HZN.AX', 0.15, False)
Stock_Trace('FMG.AX', 19.5, False)

#in money
Stock_Trace('AGL.AX', 15.31, True)
Stock_Trace('ASH.AX', 0.68, True)
Stock_Trace('TLS.AX', 4.15, True)
Stock_Trace('TCL.AX', 12.6, True)
Stock_Trace('WLE.AX', 1.48, True, "17/10/2023", 0.045)
Stock_Trace('WBC.AX', 23.05, True)
Stock_Trace('ANZ.AX', 24.68, True)



#todo: incorporate ex div dates into dictionary so stocks come up on ticker within +-1month of current date

stock_symbols = [key for key in Stock_Trace._stockDict.keys()]

# Trading hours in 24-hour format (10 am to 4 pm)
now = datetime.datetime.now()
trading_start = datetime.time(10, 0)
trading_end = datetime.time(16, 0)

fig, (plt1, plt2) = plt.subplots(2, 1, figsize=(12, 12), sharex=False)

index_error = []

#period choice is 1d, 1w, 1mo, 1yr
short_period = "1d"
long_period = "7d"

#create a pretty version of print for debugging purposes
def pprint(*input_string: str):
    final_string = ""
    for foo in input_string:
        final_string += foo
    print(len(final_string)*"=")
    print(final_string)
    print(len(final_string)*"=")
    
#runs the animate function for the specified interval and list of stock tickers
def get_normalized_prices(stock_symbols: list):
    ani = animation.FuncAnimation(fig,animate,interval=60000,cache_frame_data=False)
    plt.show()

def animate(i):
    pprint("Starting at: ", str(datetime.datetime.now()))
    
    # Fetch historical data for the required period and interval as a Pandas DataFrame made of Series
    historical_data_long = yf.download(stock_symbols, period=short_period, interval="1m")["Close"]
    historical_data_short = yf.download(stock_symbols, period=long_period, interval="1m")["Close"]
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Normalize prices to the given normalization prices
    normalization_prices = [ Stock_Trace._stockDict[x].price for x in list(historical_data_short)] #account for order that yf downloads data

    normalized_data_short = historical_data_short / normalization_prices

    normalization_prices_5d = [ Stock_Trace._stockDict[x].price for x in list(historical_data_long)] #account for order that yf downloads data

    normalized_data_long = historical_data_long / normalization_prices_5d
    
    #clearing sub plots for animation
    plt1.cla()
    plt2.cla()

    # Plot the normalized prices
    for stock_symbol in stock_symbols:

        if Stock_Trace._stockDict[stock_symbol].days_left() == None and not Stock_Trace._stockDict[stock_symbol].in_money:

            print(f"{stock_symbol} no div or not in money")
            
        else:            
            #range(normalized_data_short.index.size) gives only the count of the index instead of the time       
            i = 1

            try:
                while numpy.isnan(historical_data_short[stock_symbol][-i]):  #get rid of nans if no trades in the past minutes
                    i += 1
            except IndexError:
                pprint(f"Index Error with {stock_symbol}")
                i = -1 * (len(historical_data_short[stock_symbol]) -1)
                pass

            if len(historical_data_short[stock_symbol]) == 0:
                pprint(f"No data for {stock_symbol}")

            else:
                normalised_price_short = historical_data_short[stock_symbol][-i]/Stock_Trace._stockDict[stock_symbol].price
                buy_price = Stock_Trace._stockDict[stock_symbol].price
                current_price = historical_data_short[stock_symbol][-i]
                days_left = Stock_Trace._stockDict[stock_symbol].days_left()
                if Stock_Trace._stockDict[stock_symbol].ex_date:
                    ex_date = datetime.datetime.strftime(Stock_Trace._stockDict[stock_symbol].ex_date, '%d/%m/%Y') + f"({days_left} days)"
                else:
                    ex_date = None

                print(stock_symbol,":",round(current_price,2)," purchase:", buy_price," norm:",round(normalised_price_short,2))
                
                if Stock_Trace._stockDict[stock_symbol].div:
                    div_yield = Stock_Trace._stockDict[stock_symbol].div/current_price*100
                else:
                    div_yield = 0
                
                if normalised_price_short > low_cutoff_ratio and normalised_price_short < high_cutoff_ratio:

                    chart_label = f"{stock_symbol[0:3]} \${buy_price:.2f}({current_price:.2f}) div: {div_yield:.2f}% ex:{ex_date}"
                    
                    if Stock_Trace._stockDict[stock_symbol].in_money:                        
                        markerSymbol = 'x'
                    else:
                        markerSymbol = 'o'
                        
                    plt1.plot(range(normalized_data_long.index.size),
                        normalized_data_long[stock_symbol],
                        label=chart_label,
                        marker=markerSymbol)
                    plt2.plot(range(normalized_data_short.index.size),
                        normalized_data_short[stock_symbol],
                        label=chart_label,
                        marker=markerSymbol)

                    plt1.set_xlabel("Time")
                    plt1.set_ylabel("Normalized Price")
                    plt1.set_title(f"Normalized Prices for ASX Stocks(for last 5 days)")
                    plt1.legend(loc='upper left')
                    plt1.grid()

                    plt2.set_xlabel("Time")
                    plt2.set_ylabel("Normalized Price")
                    plt2.set_title(f"Normalized Prices for ASX Stocks(for today as of {current_time})")
                    plt2.legend(loc='upper left')
                    plt2.grid()

    for plt in [plt1, plt2]:
        plt.axhline(y=1, color='black', linestyle='--', label='Purhcase')    
        plt.axhline(y=1.01, color='red', linestyle='--', label='Target1')        
        plt.axhline(y=1.02, color='blue', linestyle='--', label='Target2')
        plt.axhline(y=1.03, color='green', linestyle='--', label='Target3')
        plt.set_yticks(numpy.arange(low_cutoff_ratio, high_cutoff_ratio, 0.01))

    
        

    
if __name__ == "__main__":
    get_normalized_prices(stock_symbols)
