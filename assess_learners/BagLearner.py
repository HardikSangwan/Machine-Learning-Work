"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt

class BagLearner(object):

    def __init__(self, learner = lrl.LinRegLearner, kwargs = {'verbose':False}, bags=20,
                 boost =  False, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.learners = []
        for i in range(self.bags):
            self.learners.append(self.learner(**self.kwargs))

    def author(self):
        return 'stang84'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        for i in range(self.bags):
            m = len(dataY) * 60 // 100
            idx = np.random.choice(len(dataY), m, replace=False)
            self.learners[i].addEvidence(dataX[idx],dataY[idx])

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        if self.bags == 0:
            return [0]*points.shape[0]

        guess = np.zeros(points.shape[0])
        for i in range(self.bags):
            guess += self.learners[i].query(points)
        guess /= self.bags
        return guess

if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
