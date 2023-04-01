"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input

    orders = pd.read_csv(orders_file)

    orders = orders.sort_values(['Date'])
    orders.loc[orders['Order'] == 'SELL', 'Shares'] *= -1
    orders.loc[orders['Date'] == '2011-06-15', 'Shares'] = 0

    sym = set(orders['Symbol'])
    sym = list(sym)
    start_date = orders['Date'].iloc[0]
    end_date = orders['Date'].iloc[-1]
    prices = get_data(sym, pd.date_range(start_date, end_date))
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)

    prices['Cash'] = 1.0
    trades = prices.copy()
    trades[:] = 0.0

    holdings = trades.copy()
    holdings.loc[start_date, 'Cash'] = start_val
    trades.loc[:, 'Cash'] = 0
    fees = 0
    fees2 = 0
    # fees2 += row[3]*prices.loc[row[0], row[1]]
    for index, row in orders.iterrows():
        fees2 += np.abs(row[3] * prices.loc[row[0], row[1]]) * impact
        trades.loc[row[0], row[1]] += row[3]
        trades.loc[row[0], 'Cash'] -= commission
        fees -= commission

    res = np.sum(trades * prices, axis=1) * -1
    trades.loc[:, 'Cash'] += res
    # fees2 = np.sum(np.abs(res))*impact

    temp = start_date
    # for index, row in holdings.iterrows():
    #     if temp == start_date:
    #         holdings.loc[index] += trades.loc[index]
    #     else:
    #         holdings.loc[index] = holdings.loc[temp] + trades.loc[index]
    #     temp = index
    holdings[]
    values = holdings * prices
    rv = np.sum(values, axis=1)
    rv[-1] += fees
    rv[-1] -= fees2
    return rv


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "orders/orders-11.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2008, 6, 1)
    daily_returns = (portvals[1:] / portvals[:-1].values) - 1
    cum_ret = (portvals[-1] / portvals[0]) - 1
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    sharpe_ratio = 252 ** .5 * (daily_returns.mean()) / std_daily_ret
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])


def author():
    return 'stang84'  # replace tb34 with your Georgia Tech username.


if __name__ == "__main__":
    test_code()
