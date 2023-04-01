#stang84
import pandas as pd
import numpy as np
import datetime as dt
import os
import math
from util import get_data, plot_data
import matplotlib.pyplot as plt
import marketsimcode as msc


def testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    price = get_data([symbol], pd.date_range(sd, ed), addSPY=False)
    price.fillna(method='ffill', inplace=True)
    price.fillna(method='bfill', inplace=True)
    a = price.values[1:]-price.values[:-1]

    orders = []
    holdings = 0
    for day in range(price.shape[0]-1):
        if a[day]>0 and holdings <1000:
            orders.append(1000-holdings)
            holdings = 1000
        elif a[day]<0 and holdings >-1000:
            orders.append(-1000-holdings)
            holdings = -1000
        else:
            orders.append(0)
    orders.append(-holdings)

    return pd.DataFrame(orders)

if __name__ == "__main__":
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    sv = 100000
    df = testPolicy(symbol = "JPM", sd = sd, ed = ed, sv = sv)
    Best = msc.compute_portvals(df, symbol = 'JPM', sd = sd, ed = ed, sv = sv, commission=0.0, impact=0.0)
    df[:] = 0
    df.iloc[0] = 1000
    Benchmark = msc.compute_portvals(df, symbol = 'JPM', sd = sd, ed = ed, sv = sv, commission=0.0, impact=0.0)


    plt.plot(Best/Best.iloc[0], "black")  # red line
    plt.plot(Benchmark/Benchmark.iloc[0], color="blue")  # blue line
    plt.savefig('figure4.png')

# price = get_data(symbol, pd.date_range(sd, ed), addSPY=False)
# symbol = "AAPL"
# newsymbol = [symbol]
#
# sd=dt.datetime(2010,1,1)
# ed=dt.datetime(2011,12,31)
# sv = 100000
# price = get_data(newsymbol, pd.date_range(sd, ed),addSPY=False)
# price.fillna(method='ffill', inplace=True)
# price.fillna(method='bfill', inplace=True)
# a = price.values[1:]-price.values[:-1]
#
# orders = []
# holdings = 0
# for day in range(price.shape[0]-1):
#     if a[day]>0  and holdings <1000:
#         orders.append(1000-holdings)
#         holdings = 1000
#     elif a[day]<0 and holdings >-1000:
#         orders.append(-1000-holdings)
#         holdings = -1000
#     else:
#         orders.append(0)
# orders.append(-holdings)
#
# return pd.DataFrame(orders)
#




#
#
#def testpolicy(symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
#    price = get_data(symbol, pd.date_range(sd, ed), addSPY=False)
#    price
## orders = []
##   holdings = {sym:0 for sym in symbols}
## for day in range(lookback+1, price.shape[0]):
##    for sym in symbols:
##        if sym == 'SPY':
##            continue
##        # Go long
##        if (sma.ix[day, sym] < .95) and (bbp.ix[day,sym]<0) and (rsi.ix[day, sym] < 30) and (rsi.ix[day, 'SPY'])> 30:
##            # stock may be oversold. index does not appear to be oversold
##            if holdings[sym] < 1000:
#
#
#
#
#

