import numpy as np
import DTLearner as dt
import RTLearner as rt
import LinRegLearner as lrl

class BagLearner(object):

    def __init__(self, learner = lrl.LinRegLearner, kwargs = {}, bags = 10, boost = False, verbose = False):
        self.learners = []
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        for i in range(self.bags):
            self.learners.append(learner(**kwargs))

    def author(self):
        return 'Zliu723' # replace tb34 with your Georgia Tech username
    
    def add_evidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        n = dataX.shape[0]
        for i in range(self.bags):
            idx = np.random.choice(n, int(n*.6)+1, replace = True)
            dataX_smp = dataX[idx]
            dataY_smp = dataY[idx]
            self.learners[i].add_evidence(dataX_smp, dataY_smp)
            if self.verbose == True:
                print ("Build learning model successfully")
                print (self.learners)
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        Y = []
        for i in range(self.bags):
            Y.append(self.learners[i].query(points))
            if self.verbose == True:
                print ("find Y successfully")
                print (Y[i])
        return np.mean(Y, axis = 0)
