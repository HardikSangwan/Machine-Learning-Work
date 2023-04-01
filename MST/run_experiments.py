#!/usr/bin/python
##  CSE6140 HW2
##  This assignment requires installation of networkx package if you want to make use of available graph data structures or you can write your own!!
##  Please feel free to modify this code or write your own
import networkx as nx
import time
import sys

class UnionFind:
    # http://www.ics.uci.edu/~eppstein/PADS/UnionFind.py

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root
        
    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r],r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest


def parseEdges(graph_file):
    with open(graph_file) as f:
        el = []
        c = 0
        for l in f:
            if c == 0:
                pass
            else:
                e = l.split()
                el.append((int(e[0]),int(e[1]),int(e[2])))
            c += 1

    g = nx.MultiGraph()
    g.add_weighted_edges_from(el)

    return g,el


def computeMST(graph,edge_list):
    # KRUSKAL ALGORITHM
    edge_list.sort(key=lambda tup: tup[2])  # sorts in place

    uf = UnionFind()
    ud = {}
    t = []
    c = 0

    for i in range(0,len(edge_list)):
        u = edge_list[i][0]
        v = edge_list[i][1]
        if ud.get((u,v),None) == None:
            ud[(u,v)] = 1  
            if uf[u] != uf[v]:
            	uf.union(u,v)
            	c += edge_list[i][2]
            	t.append((u,v,edge_list[i][2]))
    return c,uf,t


def recomputeMST(u,v,w,G,uf,mst,cost):
    if uf[u] != uf[v]:
        mst[u][v]["weight"] = w
        cost += w
        uf.union(u,v)
    else:
        if mst.get_edge_data(u,v) or mst.get_edge_data(v,u):
            d = {}
            if mst.get_edge_data(u,v):
                d = mst.get_edge_data(u,v)
                if isinstance(d,dict):
                    if w < d['weight']:
                        cost += w - d['weight']
                        mst[u][v]['weight'] = w
            if mst.get_edge_data(v,u):
                d = mst.get_edge_data(v,u)
                if isinstance(d,dict):
                    if w < d['weight']:
                        cost += w - d['weight']
                        mst[v][u]['weight'] = w
        else:
            p = nx.shortest_path(mst,u,v)
            tr = []
            for i in range(0,len(p)-1):
                tr.append((p[i],p[i+1],mst[p[i]][p[i+1]]['weight']))
            tr.sort(key=lambda tup: tup[2])  # sorts in place
            if w < tr[-1][2]:
                mst.remove_edge(tr[-1][0],tr[-1][1])
                mst.add_edge(u,v,weight=w)
                cost += w - tr[-1][2]
    return cost,uf,mst
def main():

    num_args = len(sys.argv)

    if num_args < 4:
        print("error: not enough input arguments")
        exit(1)

    graph_file = sys.argv[1]
    change_file = sys.argv[2]
    output_file = sys.argv[3]

    G,edge_list = parseEdges(graph_file)

    start_MST = time.time() 
    MSTweight,uf,t = computeMST(G,edge_list)
    total_time = (time.time() - start_MST) * 1000 

    output = open(output_file, 'w')
    output.write(str(MSTweight) + " " + str(total_time) + "\n")

    mst = nx.Graph()
    mst.add_weighted_edges_from(t)
    recomputeTime = 0

    with open(change_file, 'r') as changes:
        num_changes = changes.readline()
        new_weight = MSTweight
        for line in changes:
            #parse edge and weight
            edge_data = list(map(lambda x: int(x), line.split()))
            assert(len(edge_data) == 3)

            u,v,weight = edge_data[0], edge_data[1], edge_data[2]

            #call recomputeMST function
            start_recompute = time.time()
            new_weight, uf, mst = recomputeMST(u,v,weight,G,uf,mst,new_weight)
            total_recompute = (time.time() - start_recompute) * 1000 # to convert to milliseconds
            recomputeTime += total_recompute

            #write new weight and time to output file
            output.write(str(new_weight) + " " + str(total_recompute) + "\n")
    

if __name__ == '__main__':
    # run the experiments
    main()
