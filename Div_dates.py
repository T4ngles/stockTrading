import yfinance as yf
import datetime

# List of stock tickers
stocks = ['WBC.AX', 'ANZ.AX', 'NAB.AX', 'SUN.AX', 'CBA.AX', 'MQG.AX', 'FMG.AX', 'TLS.AX', 'BHP.AX',
          'TCL.AX', 'AGL.AX', 'APA.AX', 'NEC.AX', 'WDS.AX', 'SCG.AX', 'QBE.AX', 'ORG.AX', 'DOW.AX', 'STO.AX']

stocks = ['BHP.AX', 'AGL.AX','FMG.AX','ORG.AX','WDS.AX','NEC.AX','WAM.AX','HVN.AX','GNE.AX']

stocks = ['AGL.AX','AMP.AX','ATM.AX','ANZ.AX','BOQ.AX','BEN.AX','BSL.AX','BFL.AX','DXS.AX','FMG.AX','GPT.AX','IAG.AX','LFG.AX','MGR.AX','NAB.AX','ORG.AX','PPM.AX','QAN.AX','QBE.AX','RMC.AX','SCG.AX','SGP.AX','SUN.AX','TAH.AX','TLS.AX','URW.AX','VCX.AX','WBC.AX','WOR.AX','YAL.AX',]
stocks = ['BHP.AX','CBA.AX','CSL.AX','NAB.AX','ANZ.AX','WBC.AX','WDS.AX','MQG.AX','FMG.AX','WES.AX','WOW.AX','TLS.AX','RIO.AX','TCL.AX','STO.AX','QBE.AX','NCM.AX','WTC.AX','COL.AX','SUN.AX','CPU.AX','ORG.AX','SHL.AX','IAG.AX','MIN.AX','VAS.AX','NST.AX','FPH.AX','CAR.AX','TLC.AX','TPG.AX','AMC.AX','BSL.AX','TWE.AX','AFI.AX','SPK.AX','MCY.AX','IFT.AX','AGL.AX','ORI.AX','ARG.AX','MGOC.AX','VGS.AX','EBO.AX','MEZ.AX','IVV.AX','SDF.AX','CWY.AX','BEN.AX','QUB.AX','LLC.AX','STW.AX','CGF.AX','CHC.AX']
stocks = ['FMG.AX']
start_date = datetime.datetime(2022, 1, 1, tzinfo=None)
end_date = datetime.datetime(2023, 7, 1, tzinfo=None)

# Function to get dividend history for each stock
def get_dividend_history(ticker):
    stock = yf.Ticker(ticker)
    dividend_history = stock.dividends
    dividend_history.index = dividend_history.index.tz_localize(None)
    dividend_history = dividend_history[start_date:end_date]
    return dividend_history

# Fetch dividend payment dates for each stock
dividend_dates_dict = {}
for ticker in stocks:
    dividend_dates = get_dividend_history(ticker) #date is index and value is dividend amount should calculate the return using historical price
    dividend_dates_dict[ticker] = dividend_dates
    print("-"*30)
    print(ticker,dividend_dates_dict[ticker])

print("-"*30)
print("flattening")
# Flatten the dictionary into a list of tuples (stock name, dividend date)
dates_list = [(ticker, date, div) for ticker, divs in dividend_dates_dict.items() for date,div in divs.items()] #using items to expand the original ticker,div dictionary then to expand the div dictionary into date and div amount.
#dates_list = [(ticker, date) for ticker, dates in dividend_dates_dict.items() for date in dates]

print("-"*30)
print("sorting")
# Sort the list by dividend dates in ascending order
dates_list.sort(key=lambda x: x[1])

print("-"*30)
# Print the final list of dividend payment dates labeled with stock names
for ticker, date, div in dates_list:
    print(f"{ticker} - {date} - {div}")
