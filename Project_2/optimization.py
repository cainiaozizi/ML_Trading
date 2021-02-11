#!/usr/bin/env python
# coding: utf-8


import datetime as dt 
import numpy as np 
import matplotlib.pyplot as plt  
import pandas as pd
import os
from util import get_data, plot_data
import scipy.optimize as spo


#Preset some functions for calculations
def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns = (daily_returns/daily_returns.shift(1)) - 1
    return daily_returns

def compute_cum_returns(df):
    cum_returns = df.copy()
    cum_returns = (cum_returns.iloc[-1,]/cum_returns.iloc[0,]) - 1
    return cum_returns

def normalize_data(df):
    return df/df.iloc[0,]


'''Create f(x) to optimize'''
def sharpe_ratio(allocs,prices,risk_free_rate=0.0,frequency=252.0):
    norm_prices = normalize_data(prices)
    allocation_prices = allocs*norm_prices
    portfolio_values = allocation_prices.sum(axis = 1)    
    daily_returns_1 = compute_daily_returns(portfolio_values)
    k = np.sqrt(frequency)
    sr = k* ((daily_returns_1 - risk_free_rate).mean()/daily_returns_1.std())

    return sr*-1


def optimize_portfolio(sd,ed,syms,gen_plot):
    
    '''Read in adjusted closing prices for given symbols, date range'''
    dates = pd.date_range(sd, ed)  
    prices_all = get_data(syms, dates)  # automatically adds SPY  
    prices = prices_all[syms]  # only portfolio symbols 
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
    
    
    '''Compute the minimize function for allocation'''
    #step 1 define the Sharpe ratio shown in above 
    #step 2 set the guess_allocs, and the bounds
    guess_allocs = [(1./len(syms))] *len(syms)
    bnds = ((0.,1.),) * len(syms)
    
    #step 3 use the minimize function to calculate allocation, for optimizing the sharpe ratio
    result = spo.minimize(sharpe_ratio, guess_allocs, args =(prices,), method='SLSQP', options = {'disp':True},bounds = bnds, constraints = ({ 'type': 'eq', 'fun': lambda x: 1.0 - sum(x)}))
    allocs = result.x
    
    
    '''Conpute porfolio values after allocation'''
    norm_prices = normalize_data(prices)
    allocation_prices = allocs*norm_prices
    portfolio_values = allocation_prices.sum(axis = 1) 
    
    
    '''Compute the statistics'''
    #step 1 - compute daily return
    daily_returns_1 = compute_daily_returns(portfolio_values)
    
    #step 2 - compute stat: cr, adr, sddr, sr
    cr = compute_cum_returns(portfolio_values) #cumulative return
    adr = daily_returns_1.mean()#the average daily return
    sddr = daily_returns_1.std() #standard deviation of daily returns
    sr = adr/sddr* np.sqrt(252.0)
    
    '''Plot the data'''
    if gen_plot == True:
        df_temp = pd.concat([portfolio_values, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_temp = normalize_data(df_temp)
        ax = df_temp.plot(title = "Daily Portfolio Value vs. S&P 500" )
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend(loc='upper left')
        plt.savefig('plot.png')
    else:
        pass
    
    return allocs,cr,adr,sddr,sr



def test_code():  
    start_date = dt.datetime(2008, 6, 1) 
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD", "JPM"]  
  
    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=True)
         
    # Print statistics
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")  


if __name__ == "__main__":
    test_code() 

