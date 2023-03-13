import requests
import pandas as pd
import time
import datetime
import os
import math


def submitTradeSignals():
    # import free cash and batch csv
    accountInfo = pd.read_csv(
        r'C:\Users\tahsi\Desktop\STOCK SCREENER\Stock_Screener_Outputs\AccountStatus.csv'
    )
    freeCash = accountInfo.iloc[0, 0]
    freeBatches = accountInfo.iloc[0, 1]
    tradeAmount = freeCash / freeBatches
    # transactions list
    transactions = pd.read_csv(
        r'C:\Users\tahsi\Desktop\STOCK SCREENER\Stock_Screener_Outputs\Transactions.csv'
    )
    # import QualificationOutput
    qualifiedTrades = pd.read_csv(
        r'C:\Users\tahsi\Desktop\STOCK SCREENER\Stock_Screener_Outputs\QualificationOutput.csv'
    )

    for currentTicker in qualifiedTrades.values:
        print(freeCash)
        print(freeBatches)
        if (freeBatches <= 0):
            break
        else:
            # execute buy order
            url = 'https://collective2.com/world/apiv2/submitSignal'
            buyData = {
                "apikey": "cfCbQBsPmpPobBhDerR7uXoQmqZesYjS6bKOBNxUDBTEAb1APC",
                "systemid": "139566618",
                # 139566618
                "signal": {
                    "action": "BTO",
                    "quant": math.floor(tradeAmount / currentTicker[6]),
                    "symbol": currentTicker[1],
                    "typeofsymbol": "stock",
                    "market": 1,
                    "duration": "DAY",
                    "profittarget": currentTicker[3],
                    "stoploss": currentTicker[4]
                }
            }
            params = {}
            result = requests.post(url, params=params, json=buyData)
            print(result.text)
            # update account info
            freeBatches = freeBatches - 1
            freeCash = freeCash - tradeAmount
            # write executed trade to transactions
            transactions.loc[len(transactions)] = currentTicker
    # update transactions csv
    cwd = os.getcwd()
    os.chdir(
        'C:/Users/tahsi/Desktop/STOCK SCREENER/Stock_Screener_Outputs'
    )
    transactions.to_csv("Transactions.csv", index=False)
    # update account info csv
    accountInfo.iloc[0, 0] = freeCash
    accountInfo.iloc[0, 1] = freeBatches
    accountInfo.to_csv("AccountStatus.csv", index=False)
    os.chdir(cwd)
    print(transactions)
    print(accountInfo)
