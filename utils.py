import numpy as np
from nsepython import nsefetch
import urllib



def calculate_rsi(ticker_data, period:int = 14):
    """
    Calculates the Relative Strength Index (RSI) for a given set of data.


    Parameters:
    - data: A list or numpy array containing the historical index values.
    - period: An integer representing the time period for which to calculate the RSI. Default is 14.


    Returns:
    - rsi_values: A list of RSI values corresponding to the input data.
    """
    deltas = np.diff(ticker_data["Close"])
    
    seed = deltas[0:15]
    
    up = seed[seed >= 0].sum()/ period
    down = -seed[seed < 0].sum() / period
    rs = up / down
    rsi_values = [100.0 - (100.0 / (1.0 + rs))]

    for delta in deltas[period : ]:
        if delta > 0:
            up_val = delta
            down_val = 0.0
        else:
            up_val = 0.0
            down_val = -delta

        up = (up * (period - 1) + up_val) / period
        down = (down * (period - 1) + down_val) / period

        rs = up / down
        rsi = 100.0 - (100.0 / (1.0 + rs))
        rsi_values.append(rsi)
        rsi_values.reverse()
    return rsi_values[0]





indices ={'NIFTY 50':'NIFTY','NIFTY FINANCIAL SERVICES': 'FINNIFTY','NIFTY BANK' : 'BANKNIFTY'}

def nse_optionchain_scrapper(symbol):
    symbol = nsesymbolpurify(symbol)
    if any(x in symbol for x in indices.keys()):
        payload = nsefetch('https://www.nseindia.com/api/option-chain-indices?symbol='+str(indices.get(symbol)))
    else:
        payload = nsefetch('https://www.nseindia.com/api/option-chain-equities?symbol='+symbol)
    return payload

def nsesymbolpurify(symbol):
    symbol = symbol.replace('&','%26') #URL Parse for Stocks Like M&M Finance
    return symbol

