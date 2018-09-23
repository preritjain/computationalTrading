import pandas as pd
import ta

df = pd.read_csv('/home/manzo/PycharmProjects/BinanceAPIcheck/KLines/NEOUSDT/Binance_NEOUSDT_22 Sep, 2017-22 Sep, 2018.txt', sep = ',')
cci = ta.trend.cci(df[' High'], df[' Low'], df[' Close'], n=14, c=0.015, fillna=False)


fil = open("NEOUSDT_CCI.txt", "w")
for x in cci :
    fil.write(str(x) + "\n")
fil.close()