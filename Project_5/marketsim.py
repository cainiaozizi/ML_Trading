#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data  


# In[641]:


def author():
        return 'Zliu723' # replace tb34 with your Georgia Tech username.




# In[635]:


# def compute_portvals(
#     orders_file="./orders/orders.csv",
#     start_val=1000000,
#     commission=9.95,
#     impact=0.005,
# ):

def compute_portvals(orders_file,start_val,commission,impact):
    
    #Read the 'order' file
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    orders_df.sort_index(inplace = True)

    #Extract the start date and the end date
    start_date = min(orders_df.index)
    end_date = max(orders_df.index)
    
    #Further rrepare the "order" dataframe.
    orders_df_1 = orders_df.copy()
    
    # a. update the "Shares" column to reflect the buy sell option
    def minus_sell(a, b):
        if a == 'SELL':
            return -b
        else:
            return b
    
    # b. reset the index for later use
    orders_df_1 = orders_df_1.reset_index()
    orders_df_1['Shares'] = orders_df_1.apply(lambda x: minus_sell(x['Order'], x['Shares']), axis = 1)           
    
#     print("Order_df_1:")
#     print(orders_df_1)
    
    
     
    #Get the price per share for the stocks in the "order" file
    #remove the data for "SPY"
    #Fill the N/A values to 0
    portvals = get_data(orders_df['Symbol'].unique(), pd.date_range(start_date, end_date)) 
    portvals = portvals.drop(["SPY"],axis = 1)
    portvals.fillna(method='ffill', inplace=True)
    portvals.fillna(method='bfill', inplace=True)
    portvals.sort_index(inplace = True)
   
 
  
    #Step 1: Expand the dataframe for portval
    
    symbol_list = orders_df_1['Symbol'].unique()
    #print('symbol_list: ',symbol_list)

    #1.1 add number of shares, ending number of shares column
    for i in symbol_list:
        portvals["shares of " + i] = pd.Series(0, index = portvals.index)
        portvals["Ending shares of " + i] = pd.Series(0, index = portvals.index)
    
    # add columns for commission and impact
    portvals['commission'] = pd.Series(0, index = portvals.index)
    portvals['impact'] = pd.Series(0, index = portvals.index)
    
    # update the shares columns into the dataframe        
    for i in orders_df_1.index:
        date = orders_df_1.loc[i, 'Date']
        st = orders_df_1.loc[i, 'Symbol']
        portvals.loc[date, "shares of " + st] += orders_df_1.loc[i, 'Shares']
        portvals.loc[date, "Ending shares of " + st] += orders_df_1.loc[i, 'Shares']
        portvals.loc[date, 'commission'] += commission
        portvals.loc[date, 'impact'] += abs(orders_df_1.loc[i, 'Shares']) *portvals.loc[date, st]*impact

    
    #1.2 add the beginning cash column
    portvals["beg cash"] = pd.Series(0, index = portvals.index)
    
        
    #1.3 add the change in equity column
    for i, row in portvals.iterrows():
        portfolio_value = 0
        for s in symbol_list:
            portfolio_value += portvals.loc[i, "shares of " + s] * row[s]
        portvals.loc[i, "change in equity"] = portfolio_value
           
    
    #1.3 add and update the ending cash, ending portfolio value and total value column
    portvals["ending cash"] = pd.Series(0, index = portvals.index)
    portvals["ending portfolio value"] = pd.Series(0, index = portvals.index)
    portvals["total value"] = pd.Series(0, index = portvals.index)


    portvals_1 = portvals.copy()
    portvals_1 = portvals_1.reset_index()
    
    #create iterate to update all the columns
    
    for i in portvals_1.index:
        if i == 0:           
            portvals_1["beg cash"][0] = start_val
            portvals_1.loc[0, "ending cash"] = portvals_1.loc[0,"beg cash"] - portvals_1.loc[0,"change in equity"] - portvals_1.loc[0,"commission"] - portvals_1.loc[0,"impact"]        
            
        else:
            portvals_1.loc[i,"beg cash"] = portvals_1.loc[i-1,'ending cash']
            portvals_1.loc[i,"ending cash"] = portvals_1.loc[i,'beg cash'] - portvals_1.loc[i,"change in equity"]- portvals_1.loc[i,"commission"] - portvals_1.loc[i,"impact"]
       
            for s in symbol_list:
                portvals_1.loc[i, "Ending shares of "+s] += portvals_1.loc[i-1, "Ending shares of "+s]
                
    for i, row in portvals_1.iterrows():
        equity_value = 0
        for s in symbol_list:
            equity_value += portvals_1.loc[i, "Ending shares of " + s] * row[s]
        portvals_1.loc[i, "ending portfolio value"] = equity_value    
     
    
    for i in portvals_1.index:
        portvals_1.loc[i,"total value"] = portvals_1.loc[i,"ending portfolio value"] + portvals_1.loc[i,"ending cash"]
        
 
        

    portvals_1 = portvals_1.set_index(["index"])
    portvals_2 = portvals_1.loc[start_date:end_date, 'total value']
        

    return portvals_2


# In[638]:


# def compute_portfolio(allocs, prices, sv = 1):
#     normed = prices / prices.loc[0,]
#     alloced = normed * allocs
#     pos_vals = alloced * sv
#     port_val = pos_vals.sum(axis = 1)
#     return port_val
    
# def compute_portfolio_stats(port_val):
#     daily_ret = (port_val/port_val.shift(1)) - 1   
#     cr = (port_val[-1]/port_val[0]) - 1
#     adr = daily_ret.mean()
#     sddr = daily_ret.std()
#     sr = np.sqrt(252.0) * ((daily_ret - 0.0).mean() / sddr)
#     return cr, adr, sddr, sr


# In[642]:


def test_code():  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    Helper function to test code  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		  	   		     		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		  	   		     		  		  		    	 		 		   		 		  
    # Define input parameters  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    of = "./orders/orders2.csv"  		  	   		     		  		  		    	 		 		   		 		  
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
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		     		  		  		    	 		 		   		 		  
        0.2,  		  	   		     		  		  		    	 		 		   		 		  
        0.01,  		  	   		     		  		  		    	 		 		   		 		  
        0.02,  		  	   		     		  		  		    	 		 		   		 		  
        1.5,  		  	   		     		  		  		    	 		 		   		 		  
    ]  		  	   		     		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		     		  		  		    	 		 		   		 		  
        0.2,  		  	   		     		  		  		    	 		 		   		 		  
        0.01,  		  	   		     		  		  		    	 		 		   		 		  
        0.02,  		  	   		     		  		  		    	 		 		   		 		  
        1.5,  		  	   		     		  		  		    	 		 		   		 		  
    ]  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Date Range: {start_date} to {end_date}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		     		  		  		    	 		 		   		 		  
    print()  		  	   		     		  		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals[-1]}")  	


# In[643]:


if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    test_code()  

