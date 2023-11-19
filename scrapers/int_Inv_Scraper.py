"""
    Intelligent Investor Dividend scraper

    To make use of bs4 or scrapy and regex to pull out info from intelligent
    investor website for stocks with upcoming dividends. This will then be
    used in Live_Ticker to create Stock_Trace objects to be visualised in
    matplotlib or seaborn.

    [X]copy over the boiler plate from yts.py for the scraping utils
    [ ]create a scraping module for future use in machine learning projects
    [X]get URL request string for required page.
    [X]check out the regex required to pull out Stock data
    [ ]implement functionality from Shares onedrive sheet into this module
    [ ]feed module into Live_Ticker
	[ ]use .quantile(0.25) and 5% price to calculate suggested prices for stocks
"""

import os

from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime
from threading import Timer
import re
import yfinance as yf

#limit on market cap of stocks considered
marketCapLimit = 300

#div yield minimum threshold
divYieldMin = 0.02

#div gain price 
targetPricePercent = 0.03

#quantile for target price calc
quantileTarget = 0.4

def generateStockData():

	_extStockDict = {}
	
	print ('==============Scraping started at:' + str(datetime.now().time()))
	url = "https://www.intelligentinvestor.com.au/investment-tools/shares/dividends?page=1&size=250"
	print('url page:' + url)
	content = urllib.request.urlopen(url).read()[260000:-40000]
	soup = BeautifulSoup(content, 'lxml') #lxml is the default HTML parser can check for new ones		

	#number of stock rows in table
	numberOfStocks = len(soup.find_all('td')[::11])
	print(f"There are {numberOfStocks} stocks with dividends coming up")

	for i in range(numberOfStocks):

		#ticker symbol
		tickerStart = soup.find_all('td')[i*11+0].get_text().find('(')+1
		tickerEnd = soup.find_all('td')[i*11+0].get_text().find(')')
		tickerSymbol = soup.find_all('td')[i*11+0].get_text()[tickerStart:tickerEnd]+".AX"

		#Market Cap
		marketCap = soup.find_all('td')[i*11+2].get_text()[1:].replace(",","")

		#Dividend
		dividend = soup.find_all('td')[i*11+4].get_text().strip()
		if "¢" in dividend:
			dividend = round(float(dividend[:dividend.find("¢")])/100,3)
		
		elif "$" in dividend:
			dividend = float(dividend[dividend.find("$")+1:])

		#Dividend Gain
		if len(tickerSymbol) == 6 and int(marketCap) > marketCapLimit:		
			try:
				stockPrice = yf.download(tickerSymbol, period='5d', interval="1m")["Close"][-1]
				dividendGain = round(dividend/stockPrice,4)

				#target price
				targetDivPrice = round(dividend/targetPricePercent,2)
				targetQuartilePrice = round(yf.download(tickerSymbol, period='2y', interval="1d")["Close"].quantile(quantileTarget),2)

				targetPrice = min(targetDivPrice, targetQuartilePrice)

			except IndexError:
				print(tickerSymbol," has no price data")
				stockPrice = 0
				dividendGain = 0
				targetPrice = 0
			
		else:
			dividendGain = 0

		#Ex Date
		exDate = datetime.strptime(soup.find_all('td')[i*11+6].get_text(),'%d %b %Y')
		exDate = datetime.strftime(exDate, '%d/%m/%Y')

		#Pay Date
		payDate = datetime.strptime(soup.find_all('td')[i*11+7].get_text(),'%d %b %Y')
		payDate = datetime.strftime(payDate, '%d/%m/%Y')

		if dividendGain > 0.01:
			print(i, " ", tickerSymbol, marketCap, dividend, exDate, str(dividendGain*100)+"%","||", targetDivPrice,"||",targetQuartilePrice)
		else:
			print(i, " ", tickerSymbol, marketCap, dividend, exDate, str(dividendGain*100)+"%")
		
		if dividendGain > divYieldMin:

			_extStockDict[tickerSymbol] = {}
			_extStockDict[tickerSymbol]["ticker"] = tickerSymbol
			_extStockDict[tickerSymbol]["price"] = round(targetPrice,2)
			_extStockDict[tickerSymbol]["div"] = dividend
			_extStockDict[tickerSymbol]["ex_date"] = exDate
			_extStockDict[tickerSymbol]["in_money"] = False
			_extStockDict[tickerSymbol]["divGain"] = str(dividendGain*100)+"%"
			
			#print(i," ", _extStockDict[tickerSymbol])
	
	print(10*"#","Summary",10*"#")

	for stock in _extStockDict.items():
		print(stock[1]["ticker"], "|", stock[1]["price"], "|", stock[1]["div"], stock[1]["divGain"])
	
	return _extStockDict

#=========MAIN Function=============

if __name__ == '__main__':

	print ('It is currently:' + str(datetime.now().time()))
	
	extStockDict = generateStockData() 

	for k,v in extStockDict.items():
		print(k,v)

