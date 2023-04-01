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
df = testPolicy(symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000)
symbol='JPM'
sd=dt.datetime(2008,1,1)
ed=dt.datetime(2009,12,31)
sv=100000
commission=0.0
impact=0.0

prices = get_data([symbol], pd.date_range(sd, ed), addSPY=False)
prices.fillna(method='ffill', inplace=True)
prices.fillna(method='bfill', inplace=True)

prices['Cash'] = 1.0
trades = prices.copy()
trades[:] = 0.0

holdings = trades.copy()
holdings.loc[sd, 'Cash'] = sv
trades.loc[:, 'Cash'] = 0
fees = int(sum(df.values != 0) *commission)

#fees2 += row[3]*prices.loc[row[0], row[1]]
trades.loc[:,'JPM'] = df.values
fees2 = sum(abs(np.sum(trades * prices, axis=1))) * commission
res = np.sum(trades * prices, axis=1) * -1
trades.loc[:, 'Cash'] += res
#fees2 = np.sum(np.abs(res))*impact
#holdings[:, 'JPM'] = 0
temp = sd
for index in  range(holdings.shape[0]):
    if index == 0:
        holdings.iloc[index] += trades.iloc[index]
    else:
        holdings.iloc[index] = holdings.iloc[index-1] + trades.iloc[index]
values = holdings * prices
rv = np.sum(values, axis=1)
rv[-1] -= fees
rv[-1] -= fees2







