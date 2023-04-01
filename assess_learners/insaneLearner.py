"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np
import BagLearner as bl
import LinRegLearner as lrl

class InsaneLearner(object):

    def __init__(self, verbose=False):
        self.learners = []
        for i in range(20):
            self.learners.append(bl.BagLearner(learner = lrl.LinRegLearner, kwargs = {'verbose':False}, bags=20,
                 boost =  False, verbose=False))
    def author(self):
        return 'stang84'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        for i in range(20):
            self.learners[i].addEvidence(dataX, dataY)

    def query(self, points):
        guess = np.zeros(points.shape[0])
        for i in range(20):
            guess += self.learners[i].query(points)
        guess /= 20
        return guess

if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
