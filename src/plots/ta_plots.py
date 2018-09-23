'''
Created on 23-Sep-2018

@author: prerit
'''
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import mpl_finance


# symbol = "NEOBTC"
# start = "22 Sep, 2017"
# end = "22 Sep, 2018"
# interval = Client.KLINE_INTERVAL_15MINUTE

def plotMovAvg(symbol, start, end, klines, *args) :
    ochl = []
    list_of_open = []
    three_period_moving_ave = []
    time3 = []
    five_period_moving_ave = []
    ten_period_moving_ave = []
    time10 = []

    for kline in klines:
        time1 = int(kline[0])
        open1 = float(kline[1])
        Low = float(kline[3])
        High = float(kline[2])
        Close = float(kline[4])
        Volume = float(kline[5])
        ochl.append([time1, open1, Close, High, Low, Volume])
        # track opening prices, use for calculating moving averages
        list_of_open.append(open1)
        # Calculate three 'period' moving average - Based on Candlestick duration
        if len(list_of_open) > 2:
            price3 = 0
            for pri in list_of_open[-20:]:
                price3 += pri
            three_period_moving_ave.append(float(price3 / 20))
            time3.append(time1)
        # Perform Moving Average Calculation for 10 periods
        if len(list_of_open) > 9:
            price10 = 0
            for pri in list_of_open[-50:]:
                price10 += pri
            ten_period_moving_ave.append(float(price10 / 50))
            time10.append(time1)


    fig, ax = plt.subplots()
    mpl_finance.candlestick_ochl(ax, ochl, width=1)
    plt.plot(time3, three_period_moving_ave, color='green', label='3 Period MA - Open')
    plt.plot(time10, ten_period_moving_ave, color='blue', label='10 Period MA - Open')
    ax.set(xlabel='Date', ylabel='Price', title='{} {}-{}'.format(symbol, start, end))
    plt.legend()
    plt.savefig('Binance_movAvg_{}_{}-{}.png'.format(symbol, start, end))