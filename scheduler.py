# Create Rocketry app
from rocketry import Rocketry
import json 
from datetime import datetime as dt
import yfinance as yf
import random
import json 
from fastapi.staticfiles import StaticFiles
from nsepython import *
from utils import calculate_rsi,nse_optionchain_scrapper,nsesymbolpurify
from rocketry.conds import daily, minutely, time_of_day, time_of_week
# from talib import stream, set_compatibility


app = Rocketry(execution="async")


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


def fix_time(dt):
    "Get new time measurement function"
    start_time = time.time()
    def get_time():
        sec_since_start = time.time() - start_time
        return dt.timestamp() + sec_since_start
    return get_time

app = Rocketry(config={"time_func": fix_time(datetime.datetime(2023, 6, 12, 9, 58))})


# Create some tasks

# @app.task(minutely & time_of_day.between("9:00", "15:45") & time_of_week.between("Mon", "Fri"))
async def get_index_rsi_ema_adx():

    r1 = list(stocks_pair.items())
    random.shuffle(r1)
    stocks_pair1 = dict(r1)
    
    print("data is fetching", dt.now() )
    for i in stocks_pair1.keys():
        ticker_data = yf.download(stocks_pair[i], period = '1mo',interval = '15m')
        # print(ticker_data)
        rsi = calculate_rsi(ticker_data)
        # set_compatibility(1)
        # ema_9 = stream.EMA(ticker_data['Adj Close'].to_numpy(), timeperiod=9)
        # ema_20 = stream.EMA(ticker_data['Adj Close'].to_numpy(), timeperiod=20)
        # ema_50 = stream.EMA(ticker_data['Adj Close'].to_numpy(), timeperiod=50)
        # ema_100 = stream.EMA(ticker_data['Adj Close'].to_numpy(), timeperiod=100)
        # ema_200 = stream.EMA(ticker_data['Adj Close'].to_numpy(), timeperiod=200)
        
        # plus_di = stream.PLUS_DI(ticker_data['High'].to_numpy(), ticker_data['Low'].to_numpy(), ticker_data['Adj Close'].to_numpy())
        # minus_di = stream.MINUS_DI(ticker_data['High'].to_numpy(), ticker_data['Low'].to_numpy(), ticker_data['Adj Close'].to_numpy())
        # adx = stream.ADX(ticker_data['High'].to_numpy(), ticker_data['Low'].to_numpy(), ticker_data['Adj Close'].to_numpy())
        # set_compatibility(0)
        try:
            data = {i:{}}
            data[i]["rsi"] = rsi
            # data[i]["plus_di"] = plus_di
            # data[i]["minus_di"] = minus_di
            # data[i]["adx"] = adx
            # data[i]["ema_200"] = ema_200
            # data[i]["ema_100"] = ema_100
            # data[i]["ema_50"] = ema_50
            # data[i]["ema_20"] = ema_20
            # data[i]["ema_9"] = ema_9

            json.dump(data, open("./static/Moving_average/"+i+".json","w"),default=str,indent=4)
        except Exception as e:
            print(e)
        

    # return {"success": "Data Inserted"}




if __name__ == "__main__":
    app.run()

