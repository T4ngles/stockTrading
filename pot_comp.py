import yfinance as yf
import pandas as pd

def filter_asx_stocks(min_dividend_yield=0.03, min_total_assets=1000000000):
    all_asx_tickers = pd.read_csv('https://www.asx.com.au/asx/research/ASXListedCompanies.csv', header=1)
    asx_tickers = all_asx_tickers[all_asx_tickers != 'Not Applic']
    print(asx_tickers)
    total = len(asx_tickers)
    filtered_stocks = []
    
    for index, row in asx_tickers.iterrows():
        print(index,'/', total)
        ticker = row['ASX code'] + '.AX'
        try:
            stock_data = yf.Ticker(ticker)
            historical_data = stock_data.history(period="max")
            
            # Filter data to include only dates after January 1, 2018
            historical_data = historical_data[historical_data.index >= "2020-01-01"]
            
            # Calculate average dividend yield
            dividends = stock_data.dividends
            avg_dividend_yield = dividends.mean() / historical_data["Close"].mean()
            
            # Get balance sheet data for the stock
            balance_sheet = stock_data.balance_sheet

            # Extract the 'Total Assets' from the balance sheet
            total_assets = balance_sheet.loc['Total Assets'].tail(1).values[0]/1e9

            
            
            if avg_dividend_yield > min_dividend_yield and total_assets > min_total_assets:
                filtered_stocks.append({
                    'Ticker': ticker,
                    'Company Name': row['Company name'],
                    'Average Dividend Yield': avg_dividend_yield,
                    'Total Assets (AUD)': total_assets
                })
                print(ticker)
                print(total_assets)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    return pd.DataFrame(filtered_stocks)

filtered_stocks_df = filter_asx_stocks(min_dividend_yield=0.02, min_total_assets=10)
print(len(filtered_stocks_df), " stocks")
print(filtered_stocks_df)
