#!/usr/bin/env python
# coding: utf-8

# In[99]:


import pandas as pd
import numpy as np
import datetime as dt
import util as ut
import matplotlib.pyplot as plt


# In[100]:


def author():
    return 'Zliu723'


# In[101]:


def get_momentum(df,window):
    momentum = (df/df.shift(window)) - 1
    
    # f=momentum.plot(figsize = (20,7))
    # plt.gca()
    # plt.xlabel("Date",fontsize='15')
    # plt.ylabel("Standarized Momentum",fontsize='15')
    # plt.title("Momentum for JPM",fontsize='15')
    # plt.savefig('Momentum',bbox_inches='tight')
    
    # print("momentum:", momentum[30:40])
    return momentum


# In[102]:

def get_SMA_ratio(df,sym,window = 10):
    df_sym = df[sym]
    df1 = pd.DataFrame(index = df.index)
    df1['price'] = df_sym
    df1['rolling mean'] = df_sym.rolling(window,center=False).mean()
    df1['Price/SMA ratio'] = df1['price']/df1['rolling mean']
    df1 = df1.drop(columns=['price', 'rolling mean'])
    df2= df1
    # df2 = df1.dropna()
    
    return df2



def get_SMA(df,sym, window =10):
    
    df_sym = df[sym]
    df1 = pd.DataFrame(index = df.index)
    df1['price'] = df_sym
    df1['rolling mean'] = df_sym.rolling(window,center=False).mean()
    # df2 = df1.dropna()
    df2= df1

    # f=df2.plot(figsize = (20,7))
    # plt.gca()
    # plt.xlabel("Date",fontsize='15')
    # plt.ylabel("Normalized Price",fontsize='15')
    # plt.title("Simple Moving Average for JPM",fontsize='15')
    # plt.savefig('SMA',bbox_inches='tight')
    
    # print("SMA:", df2[:10])
    return df2


# In[103]:


def get_volatility(df,sym, window = 10):
    
    df_sym = df[sym]
    df1 = pd.DataFrame(index = df.index)
    df1['volatility'] = df_sym.rolling(window,center=False).std()*(252**0.5) #Assumming 252 trade days in a year
    # df2 = df1.dropna()
    df2= df1

    # f=df2.plot(figsize = (20,7))
    # plt.gca()
    # plt.xlabel("Date",fontsize='15')
    # plt.ylabel("Normalized Price",fontsize='15')
    # plt.title("Volatility for JPM",fontsize='15')
    # plt.savefig('Volatility',bbox_inches='tight')
    
    # print("volatility: ", df2[:10])
    return df2
    


# In[104]:


def get_CCI(df,sym, window = 10):
    df_sym = df[sym]
    
    rolling_mean = df_sym.rolling(window,center=False).mean()
    
    df_cci = pd.DataFrame(index = df.index)
    df_cci['Commodity Channel Index'] = (df_sym-rolling_mean)/(0.015 * df_sym.std()) #use 0.015 multiplier for more readable result
    # df2 = df_cci.dropna()
    df2= df1
    
    # f=df2.plot(figsize = (20,7))
    # plt.gca()
    # plt.xlabel("Date",fontsize='15')
    # plt.ylabel("Normalized Price",fontsize='15')
    # plt.title("Commodity Channel Index for JPM",fontsize='15')
    # plt.savefig('CCI',bbox_inches='tight')
    
    
    #print(df2[:10])
    return df2
    


# In[105]:


def get_bollinger_band(df,sym, window = 10):
    df_sym = df[sym]
    
    rolling_mean = df_sym.rolling(window,center=False).mean()
    rolling_std  = df_sym.rolling(window,center=False).std()
    
    #create the bollinger band
    df_bb = pd.DataFrame(index = df.index)
    df_bb['upper band'] =  rolling_mean + (2*rolling_std)
    df_bb['lower band'] =  rolling_mean - (2*rolling_std)
    df_bb['rolling mean'] =  rolling_mean
    
    #create the bollinger value
    df_bb['bollinger band value'] = (df_sym - rolling_mean) / (25 * rolling_std) #use 25 multiplier for more readable result
    
    df2= df_bb
    # df2 = df_bb.dropna()
    
    # f=df2.plot(figsize = (20,7))
    # plt.gca()
    # plt.xlabel("Date",fontsize='15')
    # plt.ylabel("Normalized Price",fontsize='15')
    # plt.title("Bollinger Band for JPM",fontsize='15')
    # plt.savefig('Bollinger',bbox_inches='tight')
    
    # print("bb_value: ", df2[:10])
    return df2['bollinger band value']
    


# In[106]:


def main():
    
    #Prepare the main dataframe
    window=10
    start_date = "2008-01-02"
    end_date = "2009-12-31"
    dates = pd.date_range(start_date,end_date)
    symbols = 'JPM'
    prices = ut.get_data([symbols],dates)
    prices.fillna(method='ffill', inplace=True)
    prices.fillna(method='bfill', inplace=True)
    prices=prices/prices.iloc[0]
    
    
#     print('dataframe prices[0:10]')
#     print(prices[0:10])
#     print()
#     print()
    
    #Momentum
    get_momentum(prices,window)
    
    #Simple Moving Average
    get_SMA(prices,symbols,window)
    
    #Volatility
    get_volatility(prices,symbols,window)
    
    #Commodity channel index
    get_CCI(prices,symbols,window)
    
    
    #Bollinger Band
    get_bollinger_band(prices,symbols,window)
    
if __name__ == "__main__":
    main()

