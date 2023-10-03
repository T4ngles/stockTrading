import yfinance as yf

# CREATE A TICKER INSTANCE PASSING TESLA AS THE TARGET COMPANY
fmg = yf.Ticker('FMG.AX')

# CALL THE MULTIPLE FUNCTIONS AVAILABLE AND STORE THEM IN VARIABLES.
actions = fmg.get_actions()
balance = fmg.get_balance_sheet()
cf = fmg.get_cashflow()
div = fmg.get_dividends()
info = fmg.get_info()
inst_holders = fmg.get_institutional_holders()
news = fmg.get_news()

# PRINT THE RESULTS
print('ACTIONS*'*20)
print(actions)

print('BALANCE*'*20)
print(balance)

print('CASH*'*20)
print(cf)

print('DIVIDENDS*'*20)
print(div)

print('INFO*'*20)
print(info)

print('HOLDERS*'*20)
print(inst_holders)

print('NEWS*'*20)
print(news)

