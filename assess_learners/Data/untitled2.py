import numpy as np
import pandas as pd
df = pd.read_csv("test.csv",header=None)

x = np.array(df.iloc[:,0:-1])
y = np.array(df.iloc[:,-1])

data = np.hstack((x,y[:, None]))

#def build_tree(x,y):
#    if x.shape[0] == 1:
#        return [-1, y, -1, -1]
#    if np.unique(y).shape[0] == 1:
#        return [-1, y[0], -1, -1]
#    data = np.hstack((x,y[:, None]))
#    data = np.transpose(data)
#    i = np.argmax(np.corrcoef(data)[-1,:-1])
#    SplitVal = np.median(data[:,i])
#    lefttree = build_tree(x[x[:,i] <= SplitVal], y[y[i] <= SplitVal])
#    righttree = build_tree(x[x[:,i] > SplitVal], y[y[i] > SplitVal])
#    root = [i, SplitVal,1, lefttree.shape[0]+1]
#    return (np.append(root,lefttree, righttree))

np.random.seed(1481090001)

def build_tree(data):
    if data.shape[0] == 1:
        return np.array([[-1, data[-1], -1, -1]])
    if np.unique(data[:,-1]).shape[0] == 1:
        return np.array([[-1, data[0,-1], -1, -1]])
    print("hi")
    i = np.argmax(np.corrcoef(np.transpose(data))[-1,:-1])
    
    SplitVal = np.median(data[:,i])
    lefttree = build_tree(data[data[:,i] <= SplitVal])
    righttree = build_tree(data[data[:,i] > SplitVal])
    root = np.array([[i, SplitVal,1, lefttree.shape[0]+1]])
    return np.append(np.append(root,lefttree, axis =0), righttree, axis=0)
out = build_tree(data)



testx = x[0,:]
def guess(x):
    idx = 0
    fact = out[idx,0]
    while fact != -1:
        if x[int(fact)] <= out[idx,1]:
            idx = idx + 1
            fact  = out[idx, 0]
        else:
            idx = int(idx + out[idx, -1])
            fact = out[idx, 0]
    return int(out[idx,1])            
print( 'guess is: ', guess(testx))