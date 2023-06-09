# Create FastAPI app
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import yfinance as yf
from talib import stream, set_compatibility
import json 
import random
import urllib
from nsepython import *
from utils import calculate_rsi,nse_optionchain_scrapper,nsesymbolpurify
app = FastAPI()

stocks_pair = {

  "NIFTY 50": "^NSEI",

  "NIFTY AUTO": "^CNXAUTO",

  "NIFTY BANK": "^NSEBANK",

  "NIFTY FINANCIAL SERVICES": "NIFTY_FIN_SERVICE.NS",

  "NIFTY FMCG": "^CNXFMCG",

    "NIFTY HEALTHCARE": "NIFTY_HEALTHCARE.NS",

  "NIFTY IT": "^CNXIT",

  "NIFTY MEDIA": "^CNXMEDIA",

  "NIFTY METAL": "^CNXMETAL",

  "NIFTY PHARMA": "^CNXPHARMA",

  "NIFTY PRIVATE BANK": "NIFTY_PVT_BANK.NS",

  "NIFTY REALTY": "^CNXREALTY",

}


# Import the Rocketry app
from scheduler import app as app_rocketry
session = app_rocketry.session
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/time")
async def get_tasks():
    return session.tasks




# def nse_optionchain_scrapper(symbol):
#     symbol = nsesymbolpurify(symbol)
#     if any(x in symbol for x in indices.keys()):
#         payload = nsefetch('https://www.nseindia.com/api/option-chain-indices?symbol='+str(indices.get(symbol)))
#     else:
#         payload = nsefetch('https://www.nseindia.com/api/option-chain-equities?symbol='+symbol)
#     return payload

# def nsesymbolpurify(symbol):
#     symbol = symbol.replace('&','%26') #URL Parse for Stocks Like M&M Finance
#     return symbol




@app.get("/get_pcr_advance_declines")
async def get_pcr_advance_decline():
    
    special_chars = {
        ' ': '%20',
        '%': '%25',
        '#': '%23',
        '&': '%26',
        '+': '%2B',
        ',': '%2C',
        '/': '%2F',
        ':': '%3A',
        ';': '%3B',
        '=': '%3D',
        '?': '%3F',
        '@': '%40',
        '[': '%5B',
        ']': '%5D',
    }

    # Manually encode the index name using the special character dictionary
    
    
    
    r1 = list(stocks_pair.items())
    random.shuffle(r1)
    stocks_pair1 = dict(r1)
    print(stocks_pair1.keys())
    
    for i in stocks_pair1.keys():
            encoded_index_name=''
            encoded_index_name = ''.join([special_chars.get(char, char) for char in i])
            
            urlopen = f"https://www.nseindia.com/api/equity-stockIndices?index={encoded_index_name}"            
            
            print(urlopen)
            symboldata = nsefetch(urlopen)["data"]

            def format_data(data):
                total_ffmc = sum([item['ffmc'] for item in data[1:]])
                formatted_data = [{'Symbol': item['symbol'], 'change': item['change'], 'weight': (
                    item['ffmc'] / total_ffmc) * 100, 'is_fno': item['meta']['isFNOSec']} for item in data[1:]]
                return formatted_data
            
            sum_weights_advance = 0
            weighted_pcr = 0
            formatted_data = format_data(symboldata)
            for item in formatted_data:
                if item['change'] > 0:
                    sum_weights_advance += item['weight']

            
            if i in ["NIFTY BANK", "NIFTY 50", "NIFTY FINANCIAL SERVICES"]:
                chain = nse_optionchain_scrapper(i)
                try:
                    weighted_pcr = pcr(chain, 0)
                except Exception as e:
                    print(".................", e)
            else:
                
                for item in formatted_data:
                    if item['is_fno']:
                        chain = nse_optionchain_scrapper(item['Symbol'])
                        weighted_pcr += (item['weight']/100) * pcr(chain, 0)
            
            try:
                data = {i:{}}
                data[i]["weighted_pcr"] = weighted_pcr
                data[i]["sum_weights_advance"] = sum_weights_advance

                json.dump(data, open("./static/weightage_&_advances/"+i+".json","w"),default=str,indent=4)
            except Exception as e:
                print(e)
            
    
    
        
    return "dine"


@app.get("/calc_ticker_data")
def calc_ticker_data() :
    symbol = "NIFTYIT.NS"  # Yahoo Finance ticker symbol for NIFTY IT

    # Fetch the stock data
    data = yf.Ticker(symbol).history(period="10d",proxy="PROXY_SERVER")
    # latest_data = data.tail(1).iloc[0]

    return data
    

    # Extract the required fields
    result = {
        "priority": 1,
        "symbol": symbol,
        "identifier": latest_data["Symbol"],
        "open": latest_data["Open"],
        "dayHigh": latest_data["High"],
        "dayLow": latest_data["Low"],
        "lastPrice": latest_data["Close"],
        "previousClose": latest_data["Close"] - latest_data["Change"],
        "change": latest_data["Change"],
        "pChange": (latest_data["Change"] / latest_data["Close"]) * 100,
        "ffmc": None,  # Not available through yfinance
        "yearHigh": None,  # Not available through yfinance
        "yearLow": None,  # Not available through yfinance
        "totalTradedVolume": None,  # Not available through yfinance
        "totalTradedValue": None,  # Not available through yfinance
        "lastUpdateTime": None,  # Not available through yfinance
        "nearWKH": None,  # Not available through yfinance
        "nearWKL": None,  # Not available through yfinance
        "perChange365d": None,  # Not available through yfinance
        "date365dAgo": None,  # Not available through yfinance
        "chart365dPath": None,  # Not available through yfinance
        "date30dAgo": None,  # Not available through yfinance
        "perChange30d": None,  # Not available through yfinance
        "chart30dPath": None,  # Not available through yfinance
        "chartTodayPath": None  # Not available through yfinance
    }

    

    # Print the result
    print(result)


if __name__ == "__main__":
    app.run()