"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import pandas as pd
import RTLearner as rt
import DTLearner as dt
import BagLearner as bl
import matplotlib.pyplot as plt
data ='Data/Istanbul2.csv'
runs = 1
maxleaf = 50
t = 100
seed=1481090
np.random.seed(seed)
# data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
data = pd.read_csv(data)
data = np.array(data)
datasize = data.shape[0]
cutoff = int(datasize * 0.6)
errTestDT = np.zeros((runs, maxleaf))
errTrainDT = np.zeros((runs, maxleaf))
errTestRT = np.zeros((runs, maxleaf))
errTrainRT = np.zeros((runs, maxleaf))
for i in range(runs):
    seed = 1481090002+i
    np.random.seed(seed)
    permutation = np.random.permutation(data.shape[0])
    col_permutation = np.random.permutation(data.shape[1] - 1)
    train_data = data[permutation[:cutoff], :]
    trainX = train_data[:, col_permutation]
    trainY = train_data[:, -1]
    test_data = data[permutation[cutoff:], :]
    testX = test_data[:, col_permutation]
    testY = test_data[:, -1]
    for leaf in range(1,maxleaf+1):
        learner = bl.BagLearner(dt.DTLearner, kwargs={"leaf_size": leaf},
                                bags=t, boost=False, verbose=False)
        #learner = dt.DTLearner(leaf_size = leaf)
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
        errTrainDT[i, leaf - 1] = rmse
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
        errTestDT[i, leaf - 1] = rmse
        #learner = rt.RTLearner(leaf_size=leaf)
        learner = bl.BagLearner(rt.RTLearner, kwargs={"leaf_size": leaf},
                                bags=t, boost=False, verbose=False)
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
        errTrainRT[i, leaf - 1] = rmse
        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
        errTestRT[i, leaf - 1] = rmse
TrainRMSEDT = np.mean(errTrainDT, axis=0)
TestRMSEDT = np.mean(errTestDT, axis=0)
TrainRMSERT = np.mean(errTrainRT, axis=0)
TestRMSERT = np.mean(errTestRT, axis=0)
d = {'DTTrainRMSE': TrainRMSEDT, 'DTTestRMSE': TestRMSEDT,'RTTrainRMSE': TrainRMSERT, 'RTTestRMSE': TestRMSERT}
df = pd.DataFrame(data=d)
ax = df.plot(title='Leaf Size vs RMSE of DT and RT {} bags'.format(t), fontsize=12)
ax.set_xlabel("Leaf Size")
ax.set_ylabel("RMSE")
plt.savefig('DTvsRT{}leaf{}.png'.format(t,maxleaf), bbox_inches='tight')
