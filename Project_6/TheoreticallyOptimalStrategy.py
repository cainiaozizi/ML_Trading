#!/usr/bin/env python
# coding: utf-8

# In[382]:


#1 Should call marketsimcode as necessary to generate the plot and statistics.
import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import util as ut
import marketsimcode as mk


# In[383]:


def author():
    return 'Zliu723' # replace tb34 with your Georgia Tech username.


# In[384]:


# 2.implementing a TheoreticallyOptimalStrategy object
class TheoreticallyOptimalStrategy(object):
    
    #3 implement testPolicy() which returns a trades data frame
    def testPolicy(self,symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        '''
        The input parameters are:
            symbol: the stock symbol to act on
            sd: A datetime object that represents the start date
            ed: A datetime object that represents the end date
            sv: Start value of the portfolio

        The output df_trades in form:   Date | Symbol | Order | Shares
        '''
        dates = pd.date_range(sd,ed)
        prices = ut.get_data([symbol],dates)
        prices.fillna(method='ffill', inplace=True)
        prices.fillna(method='bfill', inplace=True)

    #     print("prices[:10]")
    #     print(prices[:10])


        #This is for creating the dataframe for df_trades
        symbol_list = []
        date_range = []
        price_of_day = []
        order = []
        share = []

        current_shares = 0


        for i in range(len(prices.index)-1): # for i in 0 - 504
            symbol_list.append(symbol)
            date_range.append(prices.index[i])
            price_of_day.append(prices[symbol][i])

            #if today's price > tmr's price: you should buy
            if prices[symbol][i] < prices[symbol][i+1] and current_shares == 0:
                order.append("BUY")
                share.append(1000)
                current_shares += 1000
            elif prices[symbol][i] < prices[symbol][i+1] and current_shares < 0:
                order.append("BUY")
                share.append(2000)
                current_shares += 2000
            elif prices[symbol][i] < prices[symbol][i+1] and current_shares > 0:
                order.append("HOLD")
                share.append(0)
                current_shares += 0        

            #if today's price > tmr's price: you should sell
            elif prices[symbol][i] > prices[symbol][i+1] and current_shares == 0:
                order.append("SELL")
                share.append(-1000)
                current_shares += -1000
            elif prices[symbol][i] > prices[symbol][i+1] and current_shares > 0:
                order.append("SELL")
                share.append(-2000)
                current_shares += -2000
            elif prices[symbol][i] > prices[symbol][i+1] and current_shares < 0:
                order.append("HOLD")
                share.append(0)
                current_shares += 0
            #if today's price = tmr's price: you should hold the stock
            else:
                order.append("HOLD")
                share.append(0)
                current_shares += 0

        #create the dataframe to store the result
        df_trades = pd.DataFrame(index = date_range, columns = ['Symbol','Prices', 'Order', 'Shares'])
        df_trades['Symbol'] = symbol_list
        df_trades['Prices'] = price_of_day
        df_trades['Order'] = order
        df_trades['Shares'] = share

        #print("df_trades[:10]")
        #print(df_trades[:10])

        return df_trades

    #4. set up a benchmark function: buy 1000 shares in day 1 and hold it until the end
    def benchMark(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):

        dates = pd.date_range(sd,ed)
        prices = ut.get_data([symbol],dates)
        prices.fillna(method='ffill', inplace=True)
        prices.fillna(method='bfill', inplace=True)


        #This is for creating the dataframe for df_trades
        symbol_list = symbol
        date_range = [prices.index[0],prices.index[len(prices.index)-1]]
        price_of_day = [prices[symbol][0],prices[symbol][len(prices.index)-1]]
        order = ['BUY','SELL']
        share = [1000,-1000]
        

# #         print(prices.index)
#         x = len(prices.index)-1
        
#         for i in range(len(prices.index)-1):
#             symbol_list.append(symbol)
#             date_range.append(prices.index[i])
#             price_of_day.append(prices[symbol][i])

#             #for day 1 in sd, buy 1000 share
#             if i == 0:
#                 order.append("BUY")
#                 share.append(1000)
#                 current_shares += 1000
                
#             elif i == x:
#                 order.append("SELL")
#                 share.append(-1000)
#                 current_shares += 0

#             else:
#                 order.append("HOLD")
#                 share.append(0)
#                 current_shares += 0

        #create the dataframe to store the result
        df_bench = pd.DataFrame(index = date_range, columns = ['Symbol','Prices', 'Order', 'Shares'])
        df_bench['Symbol'] = symbol_list
        df_bench['Prices'] = price_of_day
        df_bench['Order'] = order
        df_bench['Shares'] = share
        
#         print(df_bench)
        return df_bench



        


# In[385]:


#5. set up a main function
def main():
    start_date = '2008-1-1'
    end_date = '2009-12-31'
    start_money = 100000
    symbols = 'JPM'
    
    tos = TheoreticallyOptimalStrategy()
    #     1. Run the testPolicy for symbol XXX
    df_trades = tos.testPolicy(symbols, start_date, end_date, start_money)
    port_vals = mk.compute_portvals(orders_file = df_trades, start_val = start_money, commission=0.00, impact=0.00)
    
#     print('port_vals')
#     print(port_vals)
    
    #     2. Run the benchmark
    df_bchm = tos.benchMark(symbols, start_date, end_date, start_money)
    port_vals_bench = mk.compute_portvals(orders_file = df_bchm, start_val = start_money, commission=0.00, impact=0.00)
    print()
    print()
    print('================')
#     print('port_vals_bench')
#     print(port_vals_bench)
    
        
    # 3. calculate:   Cumulative return of the benchmark and portfolio
    #                 Stdev of daily returns of benchmark and portfolio
    #                 Mean of daily returns of benchmark and portfolio
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = mk.compute_portfolio_stats(port_vals)
    cum_ret_b, avg_daily_ret_b, std_daily_ret_b, sharpe_ratio_b = mk.compute_portfolio_stats(port_vals_bench)
    
    
    # 4. Compare portfolio against Benchmark
    print()
    print()
    print('================')
    print(f"Date Range: {start_date} to {end_date}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print(f"Sharpe Ratio of Benchmark : {sharpe_ratio_b}") 
    print() 
    print(f"Cumulative Return of Fund: {cum_ret}") 
    print(f"Cumulative Return of Benchmark : {cum_ret_b}")  
    print()
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print(f"Standard Deviation of Benchmark : {std_daily_ret_b}")
    print()
    print(f"Average Daily Return of Fund: {avg_daily_ret}")
    print(f"Average Daily Return of Benchmark : {avg_daily_ret_b}")

    # 5.Plot
    
    port_vals_norm = port_vals/port_vals.iloc[0]
    port_vals_norm= port_vals_norm.to_frame()
    port_vals_bench_norm = port_vals_bench/port_vals_bench.iloc[0]
    port_vals_bench_norm =port_vals_bench_norm.to_frame()

    f=plt.figure(figsize=(20,10))
    plt.gca()
    port_line = plt.plot(port_vals_norm, color = 'red',label = 'Theoretically Optimal Strategy' )
    bench_line = plt.plot(port_vals_bench_norm, color = 'green',label = 'Benchmark')
    plt.xlabel("Date",fontsize='15')
    plt.ylabel("Portfolio",fontsize='15')
    plt.title("Normalized Benchmark and Value of Theoretically Optimal Strategy",fontsize='15')
    f.show()
    plt.savefig('Tos_vs_Benchmark.png',bbox_inches='tight')


# In[386]:


if __name__ == "__main__":
    main()

