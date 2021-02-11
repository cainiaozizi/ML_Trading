""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		     		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		     		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		     		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		     		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		     		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		     		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		     		  		  		    	 		 		   		 		  
or edited.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		     		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		     		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		     		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		     		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		     		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		     		  		  		    	 		 		   		 		  
import random  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		     		  		  		    	 		 		   		 		  
import util as ut

import QLearner as ql
import indicators as ind
import marketsimcode as mk
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		     		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		     		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		     		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		     		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		     		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		     		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    # constructor  		  	   		     		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Constructor method  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		     		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		     		  		  		    	 		 		   		 		  
        self.commission = commission
        self.window = 10 #for indicators
        self.indicator_features = ["momentum", "sma_ratio", "bollinger_value"]
        self.steps = 10 #for discretizing
        self.STATE_POW_BASE = 4 # for state discretizing
        self.dic_thresholds = {k: [] for k in self.indicator_features}
        self.MAX_ITERATIONS = 100 #for qLearning max iteration
        self.learner = ql.QLearner(num_states=1000,
                                num_actions = 3, 
                                alpha = 0.2, 
                                gamma = 0.9, 
                                rar = 0.5, 
                                radr = 0.99, 
                                dyna = 0,
                                verbose=False)		  	   		     		  		  		    	 		 		   		 		  

    def author(self):
        return 'Zliu723'

    #find threshold
    def discretize_thresholds(self, indicators):
        stepsize = len(indicators.index)//self.steps #floor division
        for feature in self.indicator_features:
            indicator_col = indicators[feature].sort_values()
            for i in range(self.steps):
                self.dic_thresholds[feature].append(indicator_col.iloc[(i+1)*stepsize])

    #discretize
    def discretize(self, indicator_row):
        state_num = 0
        for i, feature in enumerate(self.indicator_features):
            for j, threshold_val in enumerate(self.dic_thresholds[feature]):
                if indicator_row[feature] > threshold_val:
                    continue
                else:
                    state_num = state_num + j*(self.STATE_POW_BASE **i)
        return state_num

    #prepare indicators data
    def prepare_indicators(self, symbol = "JPM", sd =dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31)):	  	   		     		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd,ed)
        prices = ut.get_data([symbol],dates)
        prices.fillna(method='ffill', inplace=True)
        prices.fillna(method='bfill', inplace=True)
        prices = prices[[symbol]]

        indicators = prices.copy()
        indicators.drop([symbol], axis =1, inplace = True)
        indicators["momentum"] = ind.get_momentum(prices, self.window)
        indicators["sma_ratio"] = ind.get_SMA_ratio(prices, symbol, self.window)
        indicators["bollinger_value"] = ind.get_bollinger_band(prices,symbol, self.window)

        return prices, indicators

    # this method should create a QLearner, and train it for trading  		  	   		     		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="JPM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        sv=100000,  		  	   		     		  		  		    	 		 		   		 		  
    ):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Trains your strategy learner over a given time frame.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol to train on  		  	   		     		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		     		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		     		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		     		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		     		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        # add your code to do learning here  		  	   		     		  		  		    	 		 		   		 		  
        prices, indicators = self.prepare_indicators(symbol, sd= sd, ed= ed)

        self.discretize_thresholds(indicators)
        state = self.discretize(indicators.iloc[self.window -1])
        action = self.learner.querysetstate(state)

        training_set_len = len(indicators.index)
        count = 0
        res = []
        
        while count < self.MAX_ITERATIONS:
            cur_shares = 0
            df_trades = prices.copy()
            df_trades['Prices'] = df_trades[symbol]
            df_trades.drop([symbol], axis =1, inplace = True)
            df_trades['Shares'] = 0
            df_trades["Symbol"] = symbol

            for i in range(self.window, training_set_len-1):
                reward = 0
                state = self.discretize(indicators.iloc[i])
                cur_price = df_trades['Prices'].iloc[i]
                next_price = df_trades['Prices'].iloc[i+1]
                col_num = df_trades.columns.get_loc('Shares')

                if action == 0: #SHORT
                    if cur_shares == 0:
                        cur_shares = -1000
                        df_trades.iloc[i, col_num] = cur_shares
                    elif cur_shares == 1000:
                        cur_shares = -1000
                        df_trades.iloc[i, col_num] = 2 * cur_shares
                elif action == 2: #LONG
                    if cur_shares == 0:
                        cur_shares = 1000
                        df_trades.iloc[i, col_num] = cur_shares
                    elif cur_shares == -1000:
                        cur_shares = 1000
                        df_trades.iloc[i, col_num] = 2 * cur_shares
                # elif action == 1: #HOLD
                reward = reward + (next_price - cur_price) * cur_shares - self.impact*(cur_price+next_price) * abs(df_trades.iloc[i, col_num])
                action = self.learner.query(state, reward)

            share_zero_indices = df_trades[df_trades['Shares'] == 0].index
            df_trades.drop(share_zero_indices, inplace=True)
            df_trades["Order"] = ["SELL" if x <0 else "BUY" for x in df_trades['Shares']]

            count = count + 1
            port_vals = mk.compute_portvals(orders_file = df_trades, start_val=sv, commission=self.commission, impact=self.impact)
            cumul_ret = (port_vals[-1] / port_vals[0]) - 1
            res.append(cumul_ret)
            if len(res) >= 10 and abs(res[-1] - res[-2]) < 0.0001:
                break
            	  	   		     		  		  		    	 		 		   		 		  
	   		     		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		     		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		     		  		  		    	 		 		   		 		  
        self,  		  	   		     		  		  		    	 		 		   		 		  
        symbol="JPM",  		  	   		     		  		  		    	 		 		   		 		  
        sd=dt.datetime(2010, 1, 1),  		  	   		     		  		  		    	 		 		   		 		  
        ed=dt.datetime(2011, 12, 31),  		  	   		     		  		  		    	 		 		   		 		  
        sv=100000,  		  	   		     		  		  		    	 		 		   		 		  
    ):  		  	   		     		  		  		    	 		 		   		 		  
        """  		  	   		     		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
        :param symbol: The stock symbol that you trained on on  		  	   		     		  		  		    	 		 		   		 		  
        :type symbol: str  		  	   		     		  		  		    	 		 		   		 		  
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		     		  		  		    	 		 		   		 		  
        :type sd: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		     		  		  		    	 		 		   		 		  
        :type ed: datetime  		  	   		     		  		  		    	 		 		   		 		  
        :param sv: The starting value of the portfolio  		  	   		     		  		  		    	 		 		   		 		  
        :type sv: int  		  	   		     		  		  		    	 		 		   		 		  
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating  		  	   		     		  		  		    	 		 		   		 		  
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.  		  	   		     		  		  		    	 		 		   		 		  
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to  		  	   		     		  		  		    	 		 		   		 		  
            long so long as net holdings are constrained to -1000, 0, and 1000.  		  	   		     		  		  		    	 		 		   		 		  
        :rtype: pandas.DataFrame  		  	   		     		  		  		    	 		 		   		 		  
        """  	
        '''            
        The output df_trades in form:   Date | Symbol | Order | Shares | Prices
        
        
        print('Price/SMA ratio print here:')
        print(price_SMA_ratio[:10])
        print('================')
        print('momentum print here:')
        print(momentum[30:40])
        print('================')
        print('bb_value print here:')
        print(bb_value[:10])
        print('================')  	   		     		  		  		    	 		 		   		 		  
        '''  		  	   		     		  		  		    	 		 		   		 		  
        prices, indicators = self.prepare_indicators(symbol, sd=sd, ed=ed)

        df_trades = prices.copy()
        df_trades['Prices'] = df_trades[symbol]
        df_trades.drop([symbol], axis =1, inplace = True)
        df_trades['Shares'] = 0
        df_trades["Symbol"] = symbol

        cur_shares = 0
        state = self.discretize(indicators.iloc[self.window -1])
        action = self.learner.querysetstate(state)
        testing_set_len = len(indicators.index)

        for i in range(self.window, testing_set_len):
            state = self.discretize(indicators.iloc[i])
            col_num = df_trades.columns.get_loc('Shares')
            if action == 0: #SHORT
                if cur_shares == 0:
                    cur_shares = -1000
                    df_trades.iloc[i, col_num] = cur_shares
                elif cur_shares == 1000:
                    cur_shares = -1000
                    df_trades.iloc[i, col_num] = 2 * cur_shares
            elif action == 2: #LONG
                if cur_shares == 0:
                    cur_shares = 1000
                    df_trades.iloc[i, col_num] = cur_shares
                elif cur_shares == -1000:
                    cur_shares = 1000
                    df_trades.iloc[i, col_num] = 2 * cur_shares
            # elif action == 1: #HOLD
            action = self.learner.querysetstate(state)

        share_zero_indices = df_trades[df_trades['Shares'] == 0].index
        df_trades.drop(share_zero_indices, inplace=True)
        df_trades["Order"] = ["SELL" if x <0 else "BUY" for x in df_trades['Shares']]

        return df_trades		  	   		     		  		  		    	 		 		   		 		  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("One does not simply think up a strategy")  		  	   		     		  		  		    	 		 		   		 		  
