'''
Logic
1. compute the 3 indicators from indicator.py
2. set up the rules, set up the benchmark
3. compute the portvals using marketsimcode
4. set up the main function to call. compare manual strategy vs benchmark

'''
import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import util as ut
import marketsimcode as mk
import indicators as ind

class ManualStrategy(object):
    # constructor  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=9.95): 
        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		     		  		  		    	 		 		   		 		  
        self.commission = commission
        self.window = 10

    def author(self):
        return 'Zliu723' # replace tb34 with your Georgia Tech username.

    def testPolicy(self, symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        '''
        The input parameters are:
            symbol: the stock symbol to act on
            sd: A datetime object that represents the start date
            ed: A datetime object that represents the end date
            sv: Start value of the portfolio

        The output df_trades in form:   Date | Symbol | Order | Shares
        '''
        # window = 10
        dates = pd.date_range(sd,ed)
        symbols = symbol
        prices = ut.get_data([symbol],dates)
        prices.fillna(method='ffill', inplace=True)
        prices.fillna(method='bfill', inplace=True)
    #     print("prices[:20]")
    #     print(prices[:20])
    #     print(len(prices))

    # 1. compute the 3 indicators from indicator.py
    # note: first 10 days might be no tradings since they are within the window time frame and 3 indicators rerturns N/A    
        SMA = ind.get_SMA(prices,symbols,self.window)
        price_SMA_ratio = ind.get_SMA_ratio(prices,symbols,self.window)
        momentum = ind.get_momentum(prices,self.window)
        bb_value = ind.get_bollinger_band(prices,symbols,self.window)
        
        
    #     print('Price/SMA ratio print here:')
    #     print(price_SMA_ratio[:20])
    #     print(len(price_SMA_ratio))
    #     print('================')
    #     print('momentum print here:')
    #     print(momentum[:20])
    #     print(len(momentum))
    #     print('================')
    #     print('bb_value print here:')
    #     print(bb_value[:20])
    #     print('================')

        #This is for creating the dataframe for df_trades
        symbol_list = []
        date_range = []
        price_of_day = []
        order = []
        share = []

        current_shares = 0
        net_hold = 0 #net_hold = 0 no share, net_hold = 1: long position, net_hold = -1 shorted position
        buy_date = []
        sell_date = []
        
        
        #for SMA_ratio: small should buy, large should sell
        #for momemtum: negative should sell, positive should buy
        #for bb_value: small should buy, large should sell
        for i in range(len(prices.index)-1): # for i in 0 - 504
            symbol_list.append(symbol)
            date_range.append(prices.index[i])
            price_of_day.append(prices[symbol][i])

            #when you should buy
            if price_SMA_ratio['Price/SMA ratio'][i] < 0.95 or momentum[symbol][i] > 0.3 or bb_value[i] <= 0.6 and current_shares == 0:
                order.append("BUY")
                share.append(1000)
                current_shares += 1000
            elif price_SMA_ratio['Price/SMA ratio'][i] < 0.95 or momentum[symbol][i] > 0.3 or bb_value[i] <= 0.6 and current_shares < 0:
                order.append("BUY")
                share.append(2000)
                current_shares += 2000

            #when you should sell
            elif price_SMA_ratio['Price/SMA ratio'][i] > 1.0 or momentum[symbol][i] < -0.15 or bb_value[i] > 0.9 and current_shares == 0:
                order.append("SELL")
                share.append(-1000)
                current_shares += -1000
            elif price_SMA_ratio['Price/SMA ratio'][i] > 1.0 or momentum[symbol][i] < -0.15 or bb_value[i] > 0.9 and current_shares > 0:
                order.append("SELL")
                share.append(-2000)
                current_shares += -2000
                
            else:
                order.append("HOLD")
                share.append(0)
                current_shares += 0
                
                
        #create the dataframe to store the result
        df_trades = pd.DataFrame(index =date_range, columns = ['Symbol','Prices', 'Order', 'Shares'])
        df_trades['Symbol'] = symbol_list
        df_trades['Prices'] = price_of_day
        df_trades['Order'] = order
        df_trades['Shares'] = share


        # print("df_trades[:20]")
        # print(df_trades[:20])
        # print(len(df_trades))
        return df_trades

    # set up the benchmark function
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

        #create the dataframe to store the result
        df_bench = pd.DataFrame(index = date_range, columns = ['Symbol','Prices', 'Order', 'Shares'])
        df_bench['Symbol'] = symbol_list
        df_bench['Prices'] = price_of_day
        df_bench['Order'] = order
        df_bench['Shares'] = share

        # print("df_bench:")
        # print(df_bench)
        return df_bench

# set up a main function
def ManualStrategyMain(verbose=False, impact=0.0, commission=0.0):
    start_date = '2008-1-1'
    end_date = '2009-12-31'
    start_money = 100000
    symbols = 'JPM'
    ms = ManualStrategy(verbose, impact, commission)
    #     1. Run the testPolicy for symbol XXX
    df_trades = ms.testPolicy(symbols, start_date, end_date, start_money)
    port_vals = mk.compute_portvals(df_trades, start_money, commission, impact)
    
    print('port_vals')
    print(port_vals)
    
    #     2. Run the benchmark
    df_bchm = ms.benchMark(symbols, start_date, end_date, start_money)
    port_vals_bench = mk.compute_portvals(df_bchm, start_money, commission, impact)
    print()
    print()
    print('================')
    print('port_vals_bench')
    print(port_vals_bench)
    
        
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

#     # 5.Plot
    
#     port_vals_norm = port_vals/port_vals.iloc[0]
#     port_vals_norm= port_vals_norm.to_frame()
#     port_vals_bench_norm = port_vals_bench/port_vals_bench.iloc[0]
#     port_vals_bench_norm =port_vals_bench_norm.to_frame()

#     f=plt.figure(figsize=(20,10))
#     plt.gca()
#     port_line = plt.plot(port_vals_norm, color = 'red',label = 'Manual Strategy' )
#     bench_line = plt.plot(port_vals_bench_norm, color = 'green',label = 'Benchmark')
#     plt.xlabel("Date",fontsize='15')
#     plt.ylabel("Portfolio",fontsize='15')
#     plt.title("Normalized Benchmark and Value of Manual Strategy",fontsize='15')
#     f.show()
#     plt.savefig('ManualStrategy_vs_Benchmark.png',bbox_inches='tight')
#     plt.close()


if __name__ == "__main__":
    ManualStrategyMain(verbose=False, impact=0.005, commission=9.95)
