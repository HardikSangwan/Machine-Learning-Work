import numpy as np
import timeit as tottime
import math
import sys
import argparse

#Distance Calculation for Euclidean
def dis_euc(x_i,y_i,x_i_1,y_i_1):
    xd = x_i_1-x_i
    yd = y_i_1-y_i
    dist = math.sqrt(xd*xd+yd*yd)
    dist = round(dist)
    return dist

#Distance calculation for GEO
def dis_geo(x_i,y_i,x_i_1,y_i_1):
    pi = math.pi
    deg = int(math.floor(x_i))
    minn = x_i-deg
    latitude_i = pi*(deg+5.0*minn/3.0)/180.0
    deg = int(math.floor(y_i))
    minn = y_i-deg
    longitude_i = pi*(deg+5.0*minn/3.0)/180.0
    deg = int(math.floor(x_i_1))
    minn = x_i_1-deg
    latitude_i_1 = pi*(deg+5.0*minn/3.0)/180.0
    deg = int(math.floor(y_i_1))
    minn = y_i_1-deg
    longitude_i_1 = pi*(deg+5.0*minn/3.0)/180.0
    RRR = 6378.388
    q1 = math.cos(longitude_i-longitude_i_1)
    q2 = math.cos(latitude_i-latitude_i_1)
    q3 = math.cos(latitude_i+latitude_i_1)
    dist = RRR*math.acos(0.5*((1.0+q1)*q2-(1.0-q1)*q3))+1.0
    dist = round(dist)
    return dist

class MSTApprox:

    #Constructor
    def __init__(self,instance,seed,limit):
        self.instance = instance.split(".")[0]
        self.location = instance
        self.path = []
        self.tot=0.0
        self.randseed = seed
        self.timelimit = limit

    #Create MST of the TSP graph
    def mst(self,graph):
        
        graphG = np.array(graph)
        mstE = []
        vis = [0]

        while len(vis) < len(graph):
            (r,c) = np.unravel_index(graphG[vis].argmin(),graphG[vis].shape)
            vis.append(c)
            mstE.append((vis[r],c))
            visr = [(c,i) for i in vis]
        
            for (i,j) in visr:
                graphG[i][j] = float("inf")
                graphG[j][i] = float("inf")

        mstEr = [(y,x) for (x,y) in mstE]
        mstE.extend(mstEr)

        return mstE

    #Preorder Traversal. Here initial input from generate tour is the random seed, which defines the root node
    #Therefore Random seed needs to be less than dimension for given instance
    def pre(self,mstG,p):
        if p not in self.path:
            self.path.append(p)
            c = [i[1] for i in mstG if i[0] == p]
            if len(c) > 0 :
                for node in c:
                    self.pre(mstG,node)
            else:
                return

    def walk(self,graph):
        gW = []
        for i in range(0,len(self.path)-1):
            d = graph[self.path[i]][self.path[i+1]]
            gW.append((self.path[i],self.path[i+1],d))
            self.tot += d
        d = graph[self.path[-1]][self.path[0]]
        gW.append((self.path[-1],self.path[0],d))
        self.tot+=d

        return gW

    #Reading in TSP graph data
    def rdata(self):
        lineOut = []
        with open(self.location) as file1:
            next(file1)
            for l in file1:
                a = l.split(' ')
                if "TYPE:" in a[0]:
                    next(file1)
                    break
                else:
                    break
                break
            next(file1)
            for l in file1:
                d = l.split(' ')
                dist_type = d[1]
                break
            next(file1)
            next(file1)
            for l in file1:
                if l == 'EOF\n':
                    break
                line=l[:-1].split(' ')
                lineOut.append({'x':float(line[1]),'y':float(line[2])})
            
            graph = np.zeros((len(lineOut),len(lineOut)))

            for i in range(len(lineOut)):
                for j in range(len(lineOut)):
                    if i == j:
                        graph[i][j] = float("inf")
                    else:
                        if "EUC_2D" in dist_type:
                            graph[i][j] = dis_euc(lineOut[j]['x'], lineOut[j]['y'], lineOut[i]['x'], lineOut[i]['y'])
                        else:
                            graph[i][j] = dis_geo(lineOut[j]['x'], lineOut[j]['y'], lineOut[i]['x'], lineOut[i]['y'])
        return graph

    #writing output to sol file
    def wdata(self,out,tot):
        tot = (str)((int)(tot))
        with open(self.location+ "_Approx_" + str(int(self.timelimit)) + '.sol','w') as file1:
            file1.write(tot)
            file1.write('\n')
            for (x,y,z) in out:
                # file1.write(str(x) + ' ' + str(y) + ' ' + str(int(z)))
                # file1.write('\n')
                file1.write(str(x) + ', ')
            
    #writing output to trace file
    def wtrace(self,time,tot):
        with open(self.instance + "_Approx_" + str(int(self.timelimit)) + '.trace','w') as file1:
            file1.write('{:.2f} {}\n'.format(time, tot))

    #Generating tour, starting from reading data to creating MST, and then preorder sorted walk
    def generate_tour(self):
        startt = tottime.default_timer()
        self.tot = 0.0
        self.path = []
        g = self.rdata()
        e = self.mst(g)
        self.pre(e,self.randseed)
        out = self.walk(g)
        stopt = tottime.default_timer()
        self.wtrace(stopt-startt,int(self.tot))
        self.wdata(out,self.tot)

    def build_tour(instance, seed, cutoff):
        approx = MSTApprox(instance,seed, cutoff)
        approx.generate_tour()
    
"""
    def build_tour(instance='Cincinnati', algorithm='x', seed=1, limit=600):
        approx = MSTApprox(instance,seed,limit)
        approx.generate_tour()
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', type=str, dest="instance", default='Cincinnati')
    parser.add_argument('-alg', type=str, dest="algorithm", default='MSTApprox')
    parser.add_argument('-time', type=int, dest="limit", default=600)
    parser.add_argument('-seed', type=int, dest="seed", default=1)
    args = parser.parse_args()
    kwargs = vars(args).copy()
    MSTApprox.build_tour(**kwargs)
"""