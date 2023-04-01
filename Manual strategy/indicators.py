# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 02:59:25 2018
#stang84
@author: steve
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
import math
from util import get_data, plot_data
import matplotlib.pyplot as plt
#use JPM
# use SPY to inform
#The in sample/development period is January 1, 2008 to December 31 2009.
#The out of sample/testing period is January 1, 2010 to December 31 2011.

#Benchmark: The performance of a portfolio starting with $100,000 cash, investing in 1000 shares of JPM and holding that position.
#There is no limit on leverage.
sv = 100000
#Allowable positions are: 1000 shares long, 1000 shares short, 0 shares
#Transaction costs for ManualStrategy: Commission: $9.95, Impact: 0.005.
#Transaction costs for BestPossibleStrategy: Commission: $0.00, Impact: 0.00
    # Process orders



def save_data(df, dir ='nameless' , title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(dir)

def indicators(symbols = 'JPM', lookback = 14, n = 14, sd= '2008-1-1', ed =  '2009-12-31', sv = 100000):
    price = get_data([symbols], pd.date_range(sd, ed), addSPY=False)
    price.fillna(method='ffill', inplace=True)
    price.fillna(method='bfill', inplace=True)
    price /= price.values[0]
    indicator = pd.DataFrame(price.copy())

    # zero out a matrix for sma
    daily_ret = price.copy()
    daily_ret.values[1:,:] = price.values[1:,:]- price.values[:-1,:]
    daily_ret.values[0,:] = np.nan
    sma = price.rolling(window = lookback, min_periods = lookback).mean()
    sma = pd.rolling_mean(price, window=lookback, min_periods = lookback)
    indicator['SMA'] = sma


    rolling_std = price.rolling(window = lookback, min_periods =lookback).std()
    top_band = sma + (2*rolling_std)
    bottom_band = sma - (2* rolling_std)
    bbp= (price - bottom_band) / (top_band - bottom_band)
    indicator['Bollinger Band Percent'] = bbp
    sma = price/sma
    indicator['Price/SMA Ratio'] = sma

    momentum = price.copy()
    momentum.ix[n:] = (price.values[n:] / price.values[:-n]) - 1
    momentum.ix[:n] = np.nan
    indicator['Momentum'] = momentum
    #momentum.ix[-lookback:, :] = np.nan
    return indicator


if __name__ == "__main__":
    a = indicators()
    save_data( a.loc[:, ['JPM', 'SMA', 'Price/SMA Ratio']], dir ='figure1.png')
    save_data( a.loc[:, ['JPM', 'Bollinger Band Percent']], dir='figure2.png')
    save_data( a.loc[:, ['JPM', 'Momentum']], dir='figure3.png')
    sell = a.loc[:, "Price/SMA Ratio"]>1.1
    buy = a.loc[:, "Price/SMA Ratio"]<.9
    





#sma = price.copy()
#for day in range(price.shape[0]):
#    sma.ix[day,:] = 0
##    for sym in symbols:
##        sma.ix[day, sym] = 0
#
## calculate SMA
##loop over all days
#for day in range(price.shape[0]):
#    if day < lookback:
#        for sym in symbols:
#            sma.ix[day, sym] = np.nan
#        continue
#    sma.ix[day,:] = price.ix[day-lookback+1:day+1,:].sum(axis=0)/lookback
#    # loop over the lookback for this day and accumulate price
##    for sym in symbols:
##        sma.ix[day, sym] =  price.ix[day-lookback+1:day+1, sym].sum()
##        # calculate SMA for this day and symbol
##        sma.ix[day, sym] = sma.ix[day,sym]/lookback

##turn SMA into price/SMA ratio indacator
#for day in range(lookback, price.shape[0]):
#    for sym in symbols:
#        sma.ix[day, sym] = price.ix[day, sym] / sma.ix[day, sym]

## RSI
#for day in range(lookback, price.shape[0]):
#    for sym in symbols:
#        up_gain = 0
#        down_loss = 0
#    # loop over the lookback from this day and calculate
#    for prev_day in range(day - lookback +1, day +1):
#        #delta = price.ix[prev_day, sym] - price.ix[prev_day-1 , sym]
#        delta = daily_ret.ix[prev_day,sym]
#        if delta >= 0:
#            up_gain = up_gain +delta
#        else:
#            down_loss = down_loss + (-1 * delta)
#    if down_loss ==0:
#        rsi.ix[day, sym] = 100
#    else:
#        rs = (up_gain/lookback) / (down_loss/lookback)
#        rsi.ix[day, sym] = 100 - (100 / (1+rs))
#BBP
#bbp = price.copy()
#for day in range(price.shape[0]):
#    # loop over the lookbak from this day and calculate std
#    for sym in symbols:
#        bbp.ix[day,sym] = ((price.ix[day-lookback+1:day+1, sym]- sma.ix[day, sym])**2).sum()
##        for prev_day in range(day-lookback+1, day+1):
##            bbp.ix[day, sym] = bbp.ix[day, sym] + math.pow(price.ix[prev_day, sym] - sma.ix[day, sym], 2)
#        # finish calculating standard deviation for this da
#        bbp.ix[day, sym] = math.sqrt(bbp.ix[day, sym]/ (lookback-1))
#
#    bottom_band = sma.ix[day, sym] - (2 * bbp.ix[day, sym])
#    top_band = sma.ix[day, sym] + ( 2 * bbp.ix[day,sym])
#
#    bbp.ix[day, sym] = (price.ix[day, sym] - bottom_band)/(top_band- bottom_band)

#    orders = []
#   holdings = {sym:0 for sym in symbols}
#for day in range(lookback+1, price.shape[0]):
#    for sym in symbols:
#        if sym == 'SPY':
#            continue
#        # Go long
#        if (sma.ix[day, sym] < .95) and (bbp.ix[day,sym]<0) and (rsi.ix[day, sym] < 30) and (rsi.ix[day, 'SPY'])> 30:
#            # stock may be oversold. index does not appear to be oversold
#            if holdings[sym] < 1000:
#
#                holdings[sym] = holdings[sym] + 1000
#                print holdings[sym]
#                orders.append([price.index[day].date(), sym, 'BUY', 1000])
#        elif (sma.ix[day, sym] < 1.05) and (bbp.ix[day,sym]>1) and (rsi.ix[day, sym] > 70) and (rsi.ix[day, 'SPY'])< 70:
#            if holdings[sym] > -1000:
#                holdings[sym] = holdings[sym] - 1000
#                orders.append([price.index[day].date(), sym, 'SELL', 1000])
#                print 2
#        # Cross SMA and holding long, close long position
#        elif(sma.ix[day, sym] >= 1) and (sma.ix[day -1 , sym] < 1) and (holdings[sym] > 0):
#            holdings[sym] = 0
#            orders.append([price.index[day].date(), sym, 'SELL', 1000])
#            print 3
#        elif(sma.ix[day, sym] <= 1) and (sma.ix[day -1 , sym] > 1) and (holdings[sym] < 0):
#            holdings[sym] = 0
#            orders.append([price.index[day].date(), sym, 'BUY', 1000])
#            print 4
#for order in orders:
#    print "     ".join(str(x) for x in order)
    # Plot raw SPY values, rolling mean and Bollinger Bands