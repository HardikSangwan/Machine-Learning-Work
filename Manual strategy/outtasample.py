import pandas as pd
import numpy as np
import datetime as dt
import os
import math
from util import get_data, plot_data
import matplotlib.pyplot as plt
import indicators as ind
import marketsimcode as msc
#stang84


def testPolicy(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
    price = get_data([symbol], pd.date_range(sd, ed), addSPY=False)
    price.fillna(method='ffill', inplace=True)
    price.fillna(method='bfill', inplace=True)
    n = 14
    a = ind.indicators(symbols = symbol, n = n, sd = sd, ed = ed)
    orders = []
    holdings = 0
    last = sd
    for day in pd.date_range(sd, ed):
        if (a.loc[day, "Price/SMA Ratio"]<1.1 or a.loc[day, 'Bollinger Band Percent']<0 or (0>a.loc[day, 'Momentum'] and a.loc[last, 'Momentum']))and holdings <1000:
            orders.append(1000-holdings)
            holdings = 1000
        elif (a.loc[day, "Price/SMA Ratio"]>.9 or a.loc[day, 'Bollinger Band Percent']>1 or (0<a.loc[day, 'Momentum'] and a.loc[last, 'Momentum']>0))and holdings >-1000:
            orders.append(-1000-holdings)
            holdings = -1000
        else:
            orders.append(0)
        last = day

    
    dst = pd.DataFrame(orders)
    dst = dst.set_index(pd.date_range(sd, ed))
    return dst


if __name__ == "__main__":
    sd=dt.datetime(2010,1,1)
    ed=dt.datetime(2011,12,31)
    sv = 100000
    df = testPolicy(symbol = "JPM", sd = sd, ed = ed, sv = sv)
    short = df[df == -1000].index
    longg = df[df == 1000].index
    man = msc.compute_portvals(df, symbol = 'JPM', sd = sd, ed = ed, sv = sv, commission=0.0, impact=0.0)
    df1 = df.copy()
    df1[:] = 0 
    df1.iloc[0] = 1000
    Benchmark = msc.compute_portvals(df1, symbol = 'JPM', sd = sd, ed = ed, sv = sv, commission=0.0, impact=0.0)
    mannorm = man/man.iloc[0]
    Benchnorm = Benchmark/Benchmark.iloc[0]
    

    plt.figure()
    plt.plot(title ='RuleBased vs Benchmark', color= ['Blue', 'Black'])
    plt.plot(mannorm.index, mannorm, 'k')
    plt.plot(Benchnorm.index, Benchnorm, 'b')
    plt.plot(title ='RuleBased vs Benchmark', color= ['Blue', 'Black'])
#
#    for xc in df[df.values>0].index:
#        plt.axvline(x=xc, color='g', linestyle='-')
#    for xc in df[df.values<0].index:
#        plt.axvline(x=xc, color='r', linestyle='-')
    
#    d = {'Manuel': mannorm, 'Benchmark': Benchnorm}               
#    df1 = pd.DataFrame(data = d)
#    df1.plot(title ='RuleBased vs Benchmark', color= ['Blue', 'Black'])
#    xposition = [pd.to_datetime('2010-01-01'), pd.to_datetime('2015-12-31')]
#    
#    for xc in xposition:
#        plt.axvline(x=xc, color='k', linestyle='-')
#    plt.show()



