"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import pandas as pd
import DTLearner as dt
import BagLearner as bl
import matplotlib.pyplot as plt
data ='Data/Istanbul2.csv'
runs = 1
maxleaf = 150
t = 10
seed=3075634
np.random.seed(seed)
# data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
data = pd.read_csv(data)
data = np.array(data)
datasize = data.shape[0]
cutoff = int(datasize * 0.6)


errTest = np.zeros((runs, maxleaf))
errTrain = np.zeros((runs, maxleaf))
for i in range(runs):
    seed = 903075634+i
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
        learner = bl.BagLearner(dt.DTLearner, kwargs = {"leaf_size":leaf},
                                bags = t, boost = False, verbose = False)
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX)  # get the predictions
        rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
        errTrain[i, leaf - 1] = rmse

        predY = learner.query(testX)  # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
        errTest[i, leaf - 1] = rmse
TrainRMSE = np.mean(errTrain, axis=0)
TestRMSE = np.mean(errTest, axis=0)
d = {'TrainRMSE': TrainRMSE, 'TestRMSE': TestRMSE}
df = pd.DataFrame(data=d)
ax = df.plot(title='Leaf Size vs RMSE using {} bag'.format(t), fontsize=12)
ax.set_xlabel("Leaf Size")
ax.set_ylabel("RMSE")
plt.savefig('Bags{}.png'.format(t), bbox_inches='tight')
