import numpy as np

class DTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.model = []

    def author(self):
        return 'Zliu723' 

    # def printable(self):
    #     return self.verbose    
        
    def add_evidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        dataY = dataY[:, None]
        data =  np.concatenate((dataX, dataY), axis=1)
        # build and save the model
        self.model = self.build_tree(data)
        # np.set_printoptions(threshold=np.inf)
        # print(self.model)
        if self.verbose == True:
            print ("Build decision tree successfully!")


    def build_tree(self,data):
        if data.shape[0] <= self.leaf_size:
            return np.array([["Leaf", np.mean(data[:,-1]), "NA", "NA"]],dtype=object)
        if np.unique(data[:,-1]).shape[0] == 1:
            return np.array([["Leaf", np.unique(data[:,-1])[0], "NA", "NA"]],dtype=object)
        else:
            i = self.findfeature(data[:,0:-1], data[:,-1])
            SplitVal = np.median(data[:,i])
            d1 = data[data[:,i] <= SplitVal]
            if np.array_equal(d1,data) == True:
                return np.array([["Leaf", np.mean(data[:,-1]), "NA", "NA"]],dtype=object)
            lefttree = self.build_tree(d1)
            righttree = self.build_tree(data[data[:,i] > SplitVal])
            root = np.array([[i, SplitVal, 1, lefttree.shape[0] + 1]],dtype=object)
            return(np.concatenate((root, lefttree, righttree), axis=0))
    
    def findfeature(self,features,y):
        num = features.shape[1]
        max = 0
        index = 0
        for i in range(num):
            if np.correlate(features[:,i],y) > max:
                max = np.correlate(features[:,i],y)
                index = i
        return index
    
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        num = points.shape[0]
        self.Y = []
        for i in range(num):
            self.queryhelper(points[i],0)
        if self.verbose == True:
            print ("find Y successfully!")
            print (np.array(self.Y).shape)
        return np.array(self.Y)
    
    def queryhelper(self,point,index):
        node = []
        node = self.model[index,:]
        if node[0] == 'Leaf':
            self.Y.append(node[1])
            pass
        elif point[node[0]] <= node[1]:
            self.queryhelper(point,index+node[2])
        elif point[node[0]] > node[1]:
            self.queryhelper(point,index+node[3])
        elif self.verbose == True:
            print ("Can't find leaf!")

if __name__=="__main__":
    print ("the secret clue is 'zzyzx'")
