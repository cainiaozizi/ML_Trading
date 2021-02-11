import math
import sys
import time
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import InsaneLearner as it
import numpy as np
import matplotlib
matplotlib.use("Agg");
import matplotlib.pyplot as plt

kMaxLeafSize = 20

def plotDTLearner(Xtrain, Ytrain, Xtest, Ytest, verbose):
    plotData = np.array([[0,0,0]])
    for i in range(kMaxLeafSize):
        learner = dt.DTLearner(leaf_size = i)
        learner.add_evidence(Xtrain, Ytrain) # train it  		   	  			    		  		  		    	 		 		   		 		  
                                                                                                                                                                              
        # evaluate in sample  		   	  			    		  		  		    	 		 		   		 		  
        predY1 = learner.query(Xtrain) # get the predictions
        Ytrain.shape = (len(Ytrain))
        rmse1 = math.sqrt(((Ytrain - predY1) ** 2).sum()/Ytrain.shape[0])
        Ytrain.shape = (len(Ytrain))
        c1 = np.corrcoef(predY1, y=Ytrain)

        # evaluate out of sample  		   	  			    		  		  		    	 		 		   		 		  
        predY2 = learner.query(Xtest) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse2 = math.sqrt(((Ytest - predY2) ** 2).sum()/Ytest.shape[0])
        c2 = np.corrcoef(predY2, y=Ytest)

        plotData = np.vstack((plotData, np.array([[i,rmse1,rmse2]])))
        
        if (verbose):
            print (learner.author())
            print  		   	  			    		  		  		    	 		 		   		 		  
            print ("In sample results")  		   	  			    		  		  		    	 		 		   		 		  
            print ("RMSE: ", rmse1)  		   	  			    		  		  		    	 		 		   		 		  
            print ("corr: ", c1[0,1])	   	  			    		  		  		    	 		 		   		 		  
            print  		   	  			    		  		  		    	 		 		   		 		  
            print ("Out of sample results")  		   	  			    		  		  		    	 		 		   		 		  
            print ("RMSE: ", rmse2) 			    		  		  		    	 		 		   		 		  
            print ("corr: ", c[0,1])

    plotData = np.delete(plotData, (0), axis=0)
    
    # Code for plot generation
    plt.figure()
    plt.suptitle('RMSE with leaf size increase', fontsize=12)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('Rmse')
    plt.xlabel('Leaf size')
    plt.plot(plotData[:,1], label="In the sample")
    plt.plot(plotData[:,2], label="Out of the sample")
    plt.legend(loc='lower right')
    plt.savefig('Figure1.png')
    plt.clf()

def plotBagLearner(Xtrain, Ytrain, Xtest, Ytest, verbose):
    plotData = np.array([[0,0,0]])
    for i in range(kMaxLeafSize):
        learner = bl.BagLearner(learner = dt.DTLearner, kwargs = {"leaf_size":i}, bags = 20, boost = False, verbose = False)
        learner.add_evidence(Xtrain, Ytrain) # train it  		   	  			    		  		  		    	 		 		   		 		  
                                                                                                                                                                              
        # evaluate in sample  		   	  			    		  		  		    	 		 		   		 		  
        predY1 = learner.query(Xtrain) # get the predictions
        Ytrain.shape = (len(Ytrain))
        rmse1 = math.sqrt(((Ytrain - predY1) ** 2).sum()/Ytrain.shape[0])
        Ytrain.shape = (len(Ytrain))
        c1 = np.corrcoef(predY1, y=Ytrain)

        # evaluate out of sample  		   	  			    		  		  		    	 		 		   		 		  
        predY2 = learner.query(Xtest) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse2 = math.sqrt(((Ytest - predY2) ** 2).sum()/Ytest.shape[0])
        c2 = np.corrcoef(predY2, y=Ytest)

        plotData = np.vstack((plotData, np.array([[i,rmse1,rmse2]])))
        
        if (verbose):
            print (learner.author())
            print  		   	  			    		  		  		    	 		 		   		 		  
            print ("In sample results")  		   	  			    		  		  		    	 		 		   		 		  
            print ("RMSE: ", rmse1)  		   	  			    		  		  		    	 		 		   		 		  
            print ("corr: ", c1[0,1])	   	  			    		  		  		    	 		 		   		 		  
            print  		   	  			    		  		  		    	 		 		   		 		  
            print ("Out of sample results")  		   	  			    		  		  		    	 		 		   		 		  
            print ("RMSE: ", rmse2)	   	  			    		  		  		    	 		 		   		 		  
            print ("corr: ", c[0,1])

    plotData = np.delete(plotData, (0), axis=0)
    
    # Code for plot generation
    plt.figure()
    plt.suptitle('RMSE with leaf size increase', fontsize=12)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('Rmse')
    plt.xlabel('Leaf size')
    plt.plot(plotData[:100,1], label="In the sample")
    plt.plot(plotData[:100,2], label="Out of the sample")
    plt.legend(loc='lower right')
    plt.savefig('Figure2.png')
    plt.clf()

def plotDTLearnerVsRTLearner(Xtrain, Ytrain, Xtest, Ytest, verbose):
    plotData = np.array([[0,0,0,0,0]])
    timeData = np.array([[0,0,0,0,0]])
    varData = np.array([[0,0,0]])
    for i in range(kMaxLeafSize):

        # code for DTLearner
        DTlearner = dt.DTLearner(leaf_size = i)
        DtLearnTime = time.time()
        DTlearner.add_evidence(Xtrain, Ytrain) # train it
        DtLearnTime = time.time() - DtLearnTime
                                                                                                                                                                              
        # evaluate in sample
        DtQueryTime = time.time()
        predY1Dt = DTlearner.query(Xtrain) # get the predictions
        DtQueryTime = time.time() - DtQueryTime
        Ytrain.shape = (len(Ytrain))
        rmse1Dt = math.sqrt(((Ytrain - predY1Dt) ** 2).sum()/Ytrain.shape[0])
        Ytrain.shape = (len(Ytrain))

        # evaluate out of sample
        predY2Dt = DTlearner.query(Xtest) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse2Dt = math.sqrt(((Ytest - predY2Dt) ** 2).sum()/Ytest.shape[0])

        # code for RTLearner
        RTlearner = rt.RTLearner(leaf_size = i)
        RtLearnTime = time.time()
        RTlearner.add_evidence(Xtrain, Ytrain) # train it
        RtLearnTime = time.time() - RtLearnTime
                                                                                                                                                                              
        # evaluate in sample
        RtQueryTime = time.time()
        predY1Rt = RTlearner.query(Xtrain) # get the predictions
        RtQueryTime = time.time() - RtQueryTime
        Ytrain.shape = (len(Ytrain))
        rmse1Rt = math.sqrt(((Ytrain - predY1Rt) ** 2).sum()/Ytrain.shape[0])
        Ytrain.shape = (len(Ytrain))

        # evaluate out of sample
        predY2Rt = RTlearner.query(Xtest) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse2Rt = math.sqrt(((Ytest - predY2Rt) ** 2).sum()/Ytest.shape[0])

        plotData = np.vstack((plotData, np.array([[i,rmse1Dt,rmse2Dt,rmse1Rt,rmse2Rt]])))
        timeData = np.vstack((timeData, np.array([[i,DtLearnTime,DtQueryTime,RtLearnTime,RtQueryTime]])))

    for i in range(2,plotData.shape[0]):
        var1 = (plotData[i,2]/plotData[i-1,2])-1
        var2 = (plotData[i,4]/plotData[i-1,4])-1
        varData = np.vstack((varData, np.array([[i,var1,var2]])))

    plotData = np.delete(plotData, (0), axis=0)
    timeData = np.delete(timeData, (0), axis=0)
    varData = np.delete(varData, (0), axis=0)

    # Code for training set rmse plot generation
    plt.figure()
    plt.suptitle('RMSE with leaf size increase', fontsize=12)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('Rmse')
    plt.xlabel('Leaf size')
    plt.plot(plotData[:100,1], label="DTLearner training set")
    plt.plot(plotData[:100,3], label="RTLearner training set")
    plt.legend(loc='lower right')
    plt.savefig('Figure3.png')
    plt.clf()

    # Code for test set rmse plot generation
    plt.figure()
    plt.suptitle('RMSE with leaf size increase', fontsize=12)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('Rmse')
    plt.xlabel('Leaf size')
    plt.plot(plotData[:100,2], label="DTLearner test Set")
    plt.plot(plotData[:100,4], label="RTLearner test Set")
    plt.legend(loc='lower right')
    plt.savefig('Figure4.png')
    plt.clf()

    # Code for learning time plot generation
    plt.figure()
    plt.suptitle('DTLearner and RTLearner learn time performace difference', fontsize=12)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('Time')
    plt.xlabel('Leaf size')
    plt.plot(timeData[:50,1] - timeData[:50,3], label="Time difference (s)")
    plt.legend(loc='upper right')
    plt.savefig('Figure5.png')
    plt.clf()

    # Code for learning time plot generation
    plt.figure()
    plt.suptitle('DTLearner and RTLearner query time performace difference', fontsize=12)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('Time')
    plt.xlabel('Leaf size')
    plt.plot(timeData[:50,2] - timeData[:50,4], label="Time difference (s)")
    plt.legend(loc='upper right')
    plt.savefig('Figure6.png')
    plt.clf()

    # Code for rsme variation plot generation
    plt.figure()
    plt.suptitle('Variation of rmse in test set with leaf size increase', fontsize=12)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=30)
    plt.ylabel('Variation')
    plt.xlabel('Leaf size')
    plt.plot(varData[:,1], label="DTLearner rmse variation %")
    plt.plot(varData[:,2], label="RTLearner rmse variation %")
    plt.legend(loc='upper right')
    plt.savefig('Figure7.png')
    plt.clf()

def shuffleData(data, rounds):
    result = data
    randomNumbers = np.random.choice(result.shape[0]-1, result.shape[0], replace=True)
    print (randomNumbers)
    for i in range(0,rounds):
        if (result.ndim > 1):
            for i in range(0,result.shape[0]):
                randomNumber = randomNumbers[i]
                auxData = result[i,:]
                result[i,:] = result[randomNumber,:]
                result[randomNumber,:] = auxData
        else:
            for i in range(0,result.shape[0]):
                randomNumber = randomNumbers[i]
                auxData = result[i]
                result[i] = result[randomNumber]
                result[randomNumber] = auxData
    return result
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:  		   	  			    		  		  		    	 		 		   		 		  
        print ("Usage: python testlearner.py <filename>")  		   	  			    		  		  		    	 		 		   		 		  
        sys.exit(1)
    inf = open(sys.argv[1])
    # treat Instambul.csv date problem
    if "Istanbul.csv" in sys.argv[1]:
        data = np.array([list(map(str, s.strip().split(","))) for s in inf.readlines()])
        data = data[1:,1:].astype(np.float)
    else:
        data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
  		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing  		   	  			    		  		  		    	 		 		   		 		  
    train_rows = int(0.6* data.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows
  		   	  			    		  		  		    	 		 		   		 		  
    # separate out training and testing data
    Xtrain = data[:train_rows,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    Ytrain = data[:train_rows,-1]  		   	  			    		  		  		    	 		 		   		 		  
    Xtest = data[train_rows:,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    Ytest = data[train_rows:,-1] 		   	  			    		  		  		    	 		 		   		 		  

    plotDTLearner(Xtrain, Ytrain, Xtest, Ytest, False)

    plotBagLearner(Xtrain, Ytrain, Xtest, Ytest, False)

    plotDTLearnerVsRTLearner(Xtrain, Ytrain, Xtest, Ytest, False)
