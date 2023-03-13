# Data Standardization Function receives data for one ticker and formats it, removes dirty data
# Data Standardization Function should call Stock Screener at the end and pass its output
from datetime import datetime
import Qualification


def cleanData(data):

    data.reset_index(inplace=True)
    data = data[(data['date'].dt.hour >= 9) & (data['date'].dt.hour <= 15)]

    # reverses order of list
    data = data.iloc[::-1]
    result = Qualification.checkAllCond(data)
    return result
