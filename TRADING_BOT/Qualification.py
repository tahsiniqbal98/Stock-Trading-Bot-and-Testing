from wsgiref import headers
import pandas as pd
import math
import datetime


def checkAllCond(data):
    # print volume
    print(data.iloc[0, 5])
    # Volume requirements
    if (data.iloc[0, 5] < 1000000):
        return False

    volFiftyMA = (sum(data.iloc[0:50, 5])) / 50
    if (volFiftyMA < 1000000):
        return False

    # 200 MA baseline
    closeTwoHundredMA = (sum(data.iloc[0:200, 4])) / 200
    if ((data.iloc[0, 4]) < closeTwoHundredMA):
        return False
    print("PASS_1")
    
    # SSL requirements
    for x in range(1, len(data.iloc[:, 1])):
        prevHlv = 0
        prevSmaHigh = (sum(data.iloc[x:(50 + x), 2])) / 50
        prevSmaLow = (sum(data.iloc[x:(50 + x), 3])) / 50
        if ((data.iloc[x, 4]) > prevSmaHigh):
            prevHlv = 1
            startingIndex = x
            break
        elif ((data.iloc[x, 4]) < prevSmaLow):
            prevHlv = -1
            startingIndex = x
            break

    if (prevHlv < 0):
        prevSslDown = prevSmaHigh
        prevSslUp = prevSmaLow
    elif (prevHlv > 0):
        prevSslDown = prevSmaLow
        prevSslUp = prevSmaHigh
    else:
        return False

    currSmaHigh = (sum(data.iloc[0:50, 2])) / 50
    currSmaLow = (sum(data.iloc[0:50, 3])) / 50

    if ((data.iloc[0, 4]) > currSmaHigh):
        currHlv = 1
    elif ((data.iloc[0, 4]) < currSmaLow):
        currHlv = -1
    else:
        return False
    if (currHlv < 0):
        currSslDown = currSmaHigh
        currSslUp = currSmaLow
    else:
        currSslDown = currSmaLow
        currSslUp = currSmaHigh
    if not ((prevSslDown > prevSslUp) & (currSslUp > currSslDown)):
        return False
    print("PASS_2")

    # ATR(14) requirements
    prevCloses = data.iloc[:50, 4].shift(periods=-1)
    firstTerm = data.iloc[:50, 2] - data.iloc[:50, 3]
    secondTerm = abs(data.iloc[:50, 2] - prevCloses.iloc[:50])
    thirdTerm = abs(data.iloc[:50, 3] - prevCloses.iloc[:50])
    TrAtr14 = pd.concat([firstTerm, secondTerm, thirdTerm], axis=1).max(axis=1)
    currTrAtr14 = max(data.iloc[0, 2] - data.iloc[0, 3],
                      abs(data.iloc[0, 2] - data.iloc[1, 4]),
                      abs(data.iloc[0, 3] - data.iloc[1, 4]))
    prevValsArray = TrAtr14
    prevValsArray.iloc[36] = (sum(prevValsArray.iloc[36:50])) / 14
    for myIndex in range(35, -1, -1):
        prevValsArray.iloc[myIndex] = (1 / 14) * (prevValsArray.iloc[
            myIndex]) + (1 - (1 / 14)) * (prevValsArray.iloc[myIndex + 1])
    atr14 = (1 / 14) * (currTrAtr14) + (1 - (1 / 14)) * (prevValsArray.iloc[1])
    if ((data.iloc[0, 4] - data.iloc[1, 4]) > 5 * atr14):
        return False
    elif ((data.iloc[0, 4] - data.iloc[0, 1]) > 5 * atr14):
        return False
    print("PASS_3")
    # CHOP requirement

    sumAtr50 = sum(TrAtr14.iloc[0:50])
    highest = data.iloc[0:50, 2].max()
    lowest = data.iloc[0:50, 3].min()
    firstLogInput = sumAtr50 / (highest - lowest)
    chop = 100 * (math.log10(firstLogInput)) / (math.log10(50))
    if (chop >= 55):
        return False
    print("PASS_4")
    # end of all tests
    return [
        data.iloc[0, 0], data.iloc[0, 6], data.iloc[0, 5],
        (data.iloc[0, 4] + (3 * atr14)), (data.iloc[0, 4] - (2 * atr14)),
        data.iloc[0, 0] + datetime.timedelta(days=15), data.iloc[0, 4]
    ]
