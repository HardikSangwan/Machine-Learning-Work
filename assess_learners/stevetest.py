"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import BagLearner as rtl
import LinRegLearner as lrl
import sys
import pandas as pd
import DTLearner as dt
if __name__=="__main__":
    inf ='Data/Istanbul2.csv'
    seed=1481090002
    np.random.seed(seed)
    # data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    data = pd.read_csv(inf)
    data = np.array(data)

    datasize = data.shape[0]
    cutoff = int(datasize * 0.6)
    permutation = np.random.permutation(data.shape[0])
    col_permutation = np.random.permutation(data.shape[1] - 1)
    train_data = data[permutation[:cutoff], :]
    # trainX = train_data[:,:-1]
    trainX = train_data[:, col_permutation]
    trainY = train_data[:, -1]
    test_data = data[permutation[cutoff:], :]
    # testX = test_data[:,:-1]
    testX = test_data[:, col_permutation]
    testY = test_data[:, -1]

    print (data.shape)
    # compute how much of the data is training and testing
    train_rows = int(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows


    import BagLearner as bl
    # create a learner and train it
    learner = rtl.BagLearner(learner = lrl.LinRegLearner , kwargs={}, bags=20, boost=False, verbose=False) # create a LinRegLearner
    learner.addEvidence(trainX, trainY) # train it
    print learner.author()

    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE!: ", rmse
    #print 'corrasdas', np.corrcoef(predY, y=trainY)
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]