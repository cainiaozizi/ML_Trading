import pandas as pd
import numpy as np
import datetime as dt
import os
import sys

import util as ut
import marketsimcode as mk

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# import ManualStrategy as ms
import StrategyLearner as sl

def author():
    return 'Zliu723' # replace tb34 with your Georgia Tech username.

def _normalize(values):
    return values / values.iloc[0]

def Exp2Main(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), start_money = 100000,commission = 9.95):
    # setting the random seed
    np.random.seed(1234)
    
    #Strategy Learner
    sl_impact_low = sl.StrategyLearner(verbose=False, impact=0.0001)
    sl_impact_low.add_evidence(symbol='JPM', sd=sd, ed=ed, sv=start_money)
    df_trades_impact_low = sl_impact_low.testPolicy(symbol='JPM', sd=sd, ed=ed, sv=start_money)
    portvals_impact_low = mk.compute_portvals(orders_file = df_trades_impact_low, start_val=start_money, commission=commission, impact=0.0001)
    
    sl_impact_med= sl.StrategyLearner(verbose=False, impact=0.001)
    sl_impact_med.add_evidence(symbol='JPM', sd=sd, ed=ed, sv=start_money)
    df_trades_impact_med = sl_impact_med.testPolicy(symbol='JPM', sd=sd, ed=ed, sv=start_money)
    portvals_impact_med = mk.compute_portvals(orders_file = df_trades_impact_med, start_val=start_money, commission=commission, impact=0.001)
    
    sl_impact_high = sl.StrategyLearner(verbose=False, impact=0.01)
    sl_impact_high.add_evidence(symbol='JPM', sd=sd, ed=ed, sv=start_money)
    df_trades_impact_high = sl_impact_high.testPolicy(symbol='JPM', sd=sd, ed=ed, sv=start_money)
    portvals_impact_high = mk.compute_portvals(orders_file = df_trades_impact_high, start_val=start_money, commission=commission, impact=0.01)
   
    print('Strategy learner: portvals_impact_low')
    print(portvals_impact_low)
    print('================')
    print('Strategy learner: portvals_impact_med')
    print(portvals_impact_med)
    print('================')
    print('Strategy learner: portvals_impact_high')
    print(portvals_impact_high)
    print('================')
    
    
    # calculate:   Cumulative return of the benchmark and portfolio
    #              Stdev of daily returns of benchmark and portfolio
    #              Mean of daily returns of benchmark and portfolio
    cum_ret_1, avg_daily_ret_1, std_daily_ret_1, sharpe_ratio_1 = mk.compute_portfolio_stats(portvals_impact_low)
    cum_ret_2, avg_daily_ret_2, std_daily_ret_2, sharpe_ratio_2 = mk.compute_portfolio_stats(portvals_impact_med)
    cum_ret_3, avg_daily_ret_3, std_daily_ret_3, sharpe_ratio_3 = mk.compute_portfolio_stats(portvals_impact_high)
    
    
    # 4. Compare portfolio against Benchmark
    print()
    print()
    print('================')
    print(f"Date Range: {sd} to {ed}")
    print()
    print(f"Sharpe Ratio of Fund impact = 0.0001 : {sharpe_ratio_1}")
    print(f"Sharpe Ratio of Fund impact = 0.001 : {sharpe_ratio_2}")
    print(f"Sharpe Ratio of Fund impact = 0.01: {sharpe_ratio_3}")
    print() 
    print(f"Cumulative Return of Fund impact = 0.0001: {cum_ret_1}") 
    print(f"Cumulative Return of Fund impact = 0.001 : {cum_ret_2}")
    print(f"Cumulative Return of Fund impact = 0.01 : {cum_ret_3}")  
    print()
    print(f"Standard Deviation of Fund impact = 0.0001: {std_daily_ret_1}")
    print(f"Standard Deviation of Fund impact = 0.001 : {std_daily_ret_2}")
    print(f"Standard Deviation of Fund impact = 0.01 : {std_daily_ret_3}")
    print()
    print(f"Average Daily Return of Fund impact = 0.0001: {avg_daily_ret_1}")
    print(f"Average Daily Return of Fund impact = 0.001 : {avg_daily_ret_2}")
    print(f"Average Daily Return of Fund impact = 0.01 : {avg_daily_ret_3}")
    
    # 5.Plot
    #Normalize the value
    port_vals_1_norm = _normalize(portvals_impact_low)
    port_vals_2_norm = _normalize(portvals_impact_med)
    port_vals_3_norm = _normalize(portvals_impact_high)

    port_vals_1_norm= port_vals_1_norm.to_frame()
    port_vals_2_norm= port_vals_2_norm.to_frame()
    port_vals_3_norm= port_vals_3_norm.to_frame()
                                    
    # f=plt.figure(figsize=(20,10))
    plt.gca()
    port_line1, = plt.plot(port_vals_1_norm, color = 'red',label = 'impact = 0.0001' )
    port_line2, = plt.plot(port_vals_2_norm, color = 'blue',label = 'impact = 0.001')
    port_line3, = plt.plot(port_vals_3_norm, color = 'green',label = 'impact = 0.01')
    plt.legend(fontsize='15')
    plt.xlabel("Date",fontsize='15')
    plt.xticks(fontsize='14',rotation=30)
    plt.ylabel("Portfolio",fontsize='15')
    plt.title("Performance of Strategy Learner in different impact values",fontsize='15')
    # f.show()
    plt.savefig('StrategyLearner_impact_comparison.png',bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    Exp2Main(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), start_money = 100000, commission=9.95)

