import pandas as pd
import time
import datetime
import StocksListStrings
import DataStandardization
import AccountManagement
import os
import yfinance as yf

tickers = StocksListStrings.all_tickers
# tickers = StocksListStrings.smol_tickers

#Result Table for Qualified Stonks
qualifiedStocks = pd.DataFrame(columns=[
    "Datetime", "Ticker", "Volume", "TakeProfit", "StopLoss", "TimeOutExit",
    "ClosePrice"
])

#--------------------------------------------------------------------


def getTickerData():
    cwd = os.getcwd()
    #loop to cycle through all tickers
    indexCount = 0
    for x in tickers:
        #keep track of where you are in the loop
        print(x)
        # print(datetime.datetime.now().time())
        #try to get data, if valueError then go to next ticker
        try:
            data = yf.download(tickers=x, period='2mo', interval='1h')
        except ValueError:
            continue
        # skip over any stocks which didn't pull enough data
        if(len(data.index)<300):
            continue
        # drop last incomplete timestamp row 
        data = data[:-1]
        # drop unused column
        data = data.drop('Adj Close', 1)
        data.index.name = 'date'
        ticker_column_data = [x] * data.shape[0]
        #add ticker name into data set as a new column
        data.insert(5, "6. Ticker", ticker_column_data, True)
        #pass data received for one ticker into Data Standardization Script
        tickerData = DataStandardization.cleanData(data)
        if (tickerData == False):
            continue
        else:
            qualifiedStocks.loc[indexCount] = tickerData
            indexCount = indexCount - 1
    final_stocks = qualifiedStocks.sort_values(by=['Volume'], ascending=False)
    os.chdir(
        'C:/Users/tahsi/Desktop/STOCK SCREENER/Stock_Screener_Outputs'
    )
    final_stocks.to_csv("QualificationOutput.csv", index=False)
    os.chdir(cwd)
    print(final_stocks)
    # ---------------------------------------------
    # Below line is only for trading strategy on C2
    # ---------------------------------------------
    # AccountManagement.submitTradeSignals()
