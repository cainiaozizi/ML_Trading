#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime as dt
import os
import sys

import util as ut
import marketsimcode as mk

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import ManualStrategy as ms
import StrategyLearner as sl

def author():
    return 'Zliu723' # replace tb34 with your Georgia Tech username.

def _normalize(values):
    return values / values.iloc[0]

def Exp1Main(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), start_money = 100000, impact=0.005, commission = 9.95):
    # setting the random seed
    np.random.seed(1234)
    
    # Manual Strategy
    manu = ms.ManualStrategy(verbose=False, impact=impact, commission = commission)
    df_trades = manu.testPolicy(symbol="JPM", sd = sd, ed = ed, sv = start_money)
    port_vals = mk.compute_portvals(orders_file = df_trades, start_val = start_money, commission=commission, impact=impact)
    
    # Strategy Learner
    slearner = sl.StrategyLearner(verbose=False, impact=impact, commission = commission)
    slearner.add_evidence(symbol="JPM", sd=sd, ed=ed, sv=start_money)
    df_trades_sl = slearner.testPolicy(symbol='JPM', sd=sd, ed= ed, sv=start_money)
    port_vals_strategy = mk.compute_portvals(orders_file = df_trades_sl, start_val=start_money, commission=commission, impact=impact)
    
    # Benchmark
    df_bchm = manu.benchMark(symbol="JPM", sd = sd, ed = ed, sv = start_money)
    port_vals_bench = mk.compute_portvals(orders_file = df_bchm, start_val = start_money, commission=commission, impact=impact)

    print('Manual strategy: port_vals')
    print(port_vals)
    print('================')
    print('Strategy strategy: port_vals_strategy')
    print(port_vals_strategy)
    print('================')
    print('Benchmark normalized: port_vals_bench')
    print(port_vals_bench)
    
    # calculate:   Cumulative return of the benchmark and portfolio
    #              Stdev of daily returns of benchmark and portfolio
    #              Mean of daily returns of benchmark and portfolio
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = mk.compute_portfolio_stats(port_vals)
    cum_ret_sl, avg_daily_ret_sl, std_daily_ret_sl, sharpe_ratio_sl = mk.compute_portfolio_stats(port_vals_strategy)
    cum_ret_b, avg_daily_ret_b, std_daily_ret_b, sharpe_ratio_b = mk.compute_portfolio_stats(port_vals_bench)
    
    # 4. Compare portfolio against Benchmark
    print()
    print()
    print('================')
    print(f"Date Range: {sd} to {ed}")
    print()
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")
    print(f"Sharpe Ratio of Strategy : {sharpe_ratio_sl}") 
    print(f"Sharpe Ratio of Benchmark : {sharpe_ratio_b}") 
    print() 
    print(f"Cumulative Return of Fund: {cum_ret}") 
    print(f"Cumulative Return of Strategy : {cum_ret_sl}")  
    print(f"Cumulative Return of Benchmark : {cum_ret_b}")  
    print()
    print(f"Standard Deviation of Fund: {std_daily_ret}")
    print(f"Standard Deviation of Strategy : {std_daily_ret_sl}")
    print(f"Standard Deviation of Benchmark : {std_daily_ret_b}")
    print()
    print(f"Average Daily Return of Fund: {avg_daily_ret}")
    print(f"Average Daily Return of Strategy : {avg_daily_ret_sl}")
    print(f"Average Daily Return of Benchmark : {avg_daily_ret_b}")
    
    # 5.Plot
    #Normalize the value
    port_vals_norm = _normalize(port_vals)
    port_vals_strategy_norm = _normalize(port_vals_strategy)
    port_vals_bench_norm = _normalize(port_vals_bench)

    port_vals_norm= port_vals_norm.to_frame()
    port_vals_strategy_norm =port_vals_strategy_norm.to_frame()
    port_vals_bench_norm =port_vals_bench_norm.to_frame()
                                      

    f=plt.figure(figsize=(20,10))
    plt.gca()
    port_line, = plt.plot(port_vals_norm, color = 'red',label = 'Manual Strategy' )
    strategy_line, = plt.plot(port_vals_strategy_norm, color = 'blue',label = 'Strategy Learner')
    bench_line, = plt.plot(port_vals_bench_norm, color = 'green',label = 'Benchmark')
    plt.legend(fontsize='15')
    plt.xlabel("Date",fontsize='15')
    plt.xticks(fontsize='14', rotation=30)
    plt.ylabel("Portfolio",fontsize='15')
    plt.title("Normalized Benchmark vs. Manual Strategy vs. Strategy Learner",fontsize='15')
    # f.show()
    plt.savefig('ManualStrategy_vs_StrategyLearner_vs_Benchmark.png',bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    Exp1Main(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31), start_money = 100000,impact=0.005, commission = 9.95)

