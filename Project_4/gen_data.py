""""""  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
		    	 		 		   		 		    		  	   		     		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
Student Name: Zi Liu  		  	   		     		  		  		    	 		 		   		 		  
GT User ID: Zliu723   		  	   		     		  		  		    	 		 		   		 		  
GT ID: 903476881  		  	   		     		  		  		    	 		 		   		 		  
"""  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import math  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
import numpy as np  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
# this function should return a dataset (X and Y) that will work  		  	   		     		  		  		    	 		 		   		 		  
# better for linear regression than decision trees  		  	   		     		  		  		    	 		 		   		 		  
def best_4_lin_reg(seed=1489683273):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		     		  		  		    	 		 		   		 		  
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		     		  		  		    	 		 		   		 		  
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param seed: The random seed for your data generation.  		  	   		     		  		  		    	 		 		   		 		  
    :type seed: int  		  	   		     		  		  		    	 		 		   		 		  
    :return: Returns data that performs significantly better with LinRegLearner than DTLearner.  		  	   		     		  		  		    	 		 		   		 		  
    :rtype: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    np.random.seed(seed)  		  	   		     		  		  		    	 		 		   		 		  
 	#determine the X array dimension - how many Xs and how many rows
    column = np.random.randint(2, high = 10+1)
    row = np.random.randint(10,high = 1000+1)

    #create the X
    X = np.random.random(size =(row,column))*200 - 100

    #create the Y
    Y = np.sum(X, axis = 1)
    slope = np.random.random()
    intercept = np.random.random()
    Y_final = slope*Y + intercept

    return X, Y_final  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def best_4_dt(seed=1489683273):  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		     		  		  		    	 		 		   		 		  
    The data set should include from 2 to 10 columns in X, and one column in Y.  		  	   		     		  		  		    	 		 		   		 		  
    The data should contain from 10 (minimum) to 1000 (maximum) rows.  		  	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
    :param seed: The random seed for your data generation.  		  	   		     		  		  		    	 		 		   		 		  
    :type seed: int  		  	   		     		  		  		    	 		 		   		 		  
    :return: Returns data that performs significantly better with DTLearner than LinRegLearner.  		  	   		     		  		  		    	 		 		   		 		  
    :rtype: numpy.ndarray  		  	   		     		  		  		    	 		 		   		 		  
    """  		  	   		     		  		  		    	 		 		   		 		  
    np.random.seed(seed)  		  	   		     		  		  		    	 		 		   		 		  
    #determine the X array dimension - how many Xs and how many rows
    column = np.random.randint(2, high = 10+1)
    row = np.random.randint(10,high = 1000+1)

    #create the X
    X = np.random.random(size =(row,column))*200 - 100

    #create the Y
    Y = X[:,0] + np.sin(X[:,-1]) + X[:,-2]**2 + X[:,-3]**3

    return X,Y  		  	   		     		  		  		    	 		 		   		 		  
     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
def author():  		  	   		     		  		  		    	 		 		   		 		  
  	  	   		     		  		  		    	 		 		   		 		  
    return "Zliu723"  		  	   		     		  		  		    	 		 		   		 		  


  	 	   		     		  		  		    	 		 		   		 		  
  		  	   		     		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		     		  		  		    	 		 		   		 		  
    print("they call me Tim.")  		  	   		     		  		  		    	 		 		   		 		  
