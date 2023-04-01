# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:29:23 2018

@author: steve
"""
orders_file="./orders/orders.csv"
start_val=1000000
commission=9.95
impact=0.005
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
