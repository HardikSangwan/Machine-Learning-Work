"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np

class DTLearner(object):

    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.table = None

    def author(self):
        return 'stang84' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """


        # slap on 1s column so linear regression finds a constant term
        newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        newdataX[:,0:dataX.shape[1]]=dataX

        def build_tree(data):
            if np.unique(data[:, -1]).shape[0] == 1:
                return np.array([[-1, data[0, -1], -1, -1]])
            if data.shape[0] <= self.leaf_size:
                return np.array([[-1, data[:, -1].mean(), -1, -1]])
            i = np.argmax(np.corrcoef(np.transpose(data))[-1, :-1])
            SplitVal = np.median(data[:, i])
            if np.unique(data[:, i]).size == 1:
                return np.array([[-1, data[:, -1].mean(), -1, -1]])

            if (data[:, i] <= SplitVal).all():
                if not ((data[:, i] < SplitVal).all()):
                    SplitVal = SplitVal - .0000001
                    lefttree = build_tree(data[data[:, i] < SplitVal])
                    righttree = build_tree(data[data[:, i] >= SplitVal])
                else:
                    # print("some")
                    return np.array([[-1, data[0, -1], -1, -1]])

            elif (data[:, i] >= SplitVal).all():
                # print("all right")
                if not ((data[:, i] > SplitVal).all()):
                    lefttree = build_tree(data[data[:, i] <= SplitVal])
                    righttree = build_tree(data[data[:, i] > SplitVal])
                else:
                    return np.array([[-1, data[0, -1], -1, -1]])
            else:
                lefttree = build_tree(data[data[:, i] <= SplitVal])
                righttree = build_tree(data[data[:, i] > SplitVal])
            # print(SplitVal)
            root = np.array([[i, SplitVal, 1, lefttree.shape[0] + 1]], dtype='f')
            return np.append(np.append(root, lefttree, axis=0), righttree, axis=0)

        data = np.hstack((dataX, dataY[:, None]))
        self.table = build_tree(data)

        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """

        def guess(x):
            idx = 0
            fact = self.table[idx, 0]
            while fact != -1:
                if x[int(fact)] <= self.table[idx, 1]:
                    idx = idx + 1
                    fact = self.table[idx, 0]
                else:
                    idx = int(idx + self.table[idx, -1])
                    fact = self.table[idx, 0]
            return self.table[idx, 1]

        dst = []
        for i in points:
            dst.append(guess(i))
        return dst

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
