# uses the date_to_milliseconds and interval_to_milliseconds functions
# https://gist.github.com/sammchardy/3547cfab1faf78e385b3fcb83ad86395
# https://gist.github.com/sammchardy/fcbb2b836d1f694f39bddd569d1c16fe

from binance.client import Client
import time
import json
from timeUtil import date_to_milliseconds, interval_to_milliseconds
import Binance.config as config
from plots.ta_plots import *

def get_historical_klines(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Binance
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
    """
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 500

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    start_ts = date_to_milliseconds(start_str)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data

def saveToCSV(symbol, start, end, klines):
    with open('../data/Binance_{}_{}-{}.csv'.format(symbol, start, end), 'w') as f:
        f.write('Time, Open, High, Low, Close, Volume\n')
        
        for kline in klines:
            #print(kline)
            time1 = int(kline[0])
            open1 = float(kline[1])
            Low = float(kline[3])
            High = float(kline[2])
            Close = float(kline[4])
            Volume = float(kline[5])
            format_kline = "{}, {}, {}, {}, {}, {}\n".format(time1, open1, High, Low, Close, Volume)
            f.write(format_kline)


def saveToJSON(symbol, interval, start, end, Klines) :
    # open a file with filename including symbol, interval and start and end converted to milliseconds
    with open(
            "Binance_{}_{}_{}-{}.json".format(
                symbol,
                interval,
                date_to_milliseconds(start),
                date_to_milliseconds(end)
            ),
            'w'  # set file write mode
    ) as f:
        f.write(json.dumps(Klines))
        
        
        
        
# fp = open('key.json','r')
# keys = json.load(fp)
# 
client = Client(config.api_key, config.api_secret)
# # get market depth
# client = Client("", "")
print(interval_to_milliseconds(Client.KLINE_INTERVAL_1MINUTE))
klines = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 Sep, 2018", "23 Sep, 2018")
symbol = 'ETHUSDT'
interval = Client.KLINE_INTERVAL_30MINUTE
start = "1 Sep, 2018"
end = "23 Sep, 2018"
plotMovAvg(symbol, start, end, klines)
# saveToCSV(symbol, start, end, klines)
# #print(klines)
# # open a file with filename including symbol, interval and start and end converted to milliseconds
# with open(
#     "../data/Binance_{}_{}_{}-{}.json".format(
#        "ETHUSDT", Client.KLINE_INTERVAL_30MINUTE, date_to_milliseconds("1 Sep, 2018"), date_to_milliseconds("23 Sep, 2018")),
#     'w' # set file write mode
# ) as f:
#     f.write(json.dumps(klines))
print('done')