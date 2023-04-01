import sys
import math
import time

global output_trace

def addBestCost(cost, timeStamp, ot):
    ot.write(str(round(timeStamp, 2)) + ", " + str(cost) + "\n")

def dis_euc(x_i,y_i,x_i_1,y_i_1):
    xd = x_i_1-x_i
    yd = y_i_1-y_i
    dist = math.sqrt(xd*xd+yd*yd)
    dist = round(dist)
    return dist

def dis_geo(x_i,y_i,x_i_1,y_i_1):
    pi = math.pi
    if x_i >= 0: 
        deg = int(math.floor(x_i))
    else:
        deg = int(math.ceil(x_i))
    minn = x_i-deg
    latitude_i = pi*(deg+5.0*minn/3.0)/180.0

    if y_i >= 0: 
        deg = int(math.floor(y_i))
    else:
        deg = int(math.ceil(y_i))
    minn = y_i-deg
    longitude_i = pi*(deg+5.0*minn/3.0)/180.0


    if (x_i_1 >= 0): 
        deg = int(math.floor(x_i_1))
    else:
        deg = int(math.ceil(x_i_1))
    minn = x_i_1-deg
    latitude_i_1 = pi*(deg+5.0*minn/3.0)/180.0
    
    if (y_i_1 >= 0): 
        deg = int(math.floor(y_i_1))
    else:
        deg = int(math.ceil(y_i_1))
    minn = y_i_1-deg
    longitude_i_1 = pi*(deg+5.0*minn/3.0)/180.0
    RRR = 6378.388
    q1 = math.cos(longitude_i-longitude_i_1)
    q2 = math.cos(latitude_i-latitude_i_1)
    q3 = math.cos(latitude_i+latitude_i_1)
    dist = RRR*math.acos(0.5*((1.0+q1)*q2-(1.0-q1)*q3))+1.0
    dist = round(dist)
    return dist

best_cost = 0

def reduce(size, w, row, col, rowred, colred):
    reductionValue = 0
    for i in range(size):
        temp = math.inf
        for j in range(size):
            temp = min(temp, w[row[i]][col[j]])
        if temp > 0:
            for j in range(size):
                if w[row[i]][col[j]] < math.inf:
                    w[row[i]][col[j]] -= temp
            reductionValue += temp
        rowred[i] = temp
    for j in range(size):
        temp = math.inf
        for i in range(size):
            temp = min(temp, w[row[i]][col[j]])
        if temp > 0:
            for i in range(size):
                if w[row[i]][col[j]] < math.inf:
                    w[row[i]][col[j]] -= temp
            reductionValue += temp
        colred[j] = temp
    return reductionValue


def bestEdge(size, w, row, col):
    mosti = -math.inf
    row_index = 0
    col_index = 0

    for i in range(size):
        for j in range(size):
            if not w[row[i]][col[j]]:
                min_row_elem = math.inf
                zeroes = 0
                for k in range(size):
                    if w[row[i]][col[k]] == 0:
                        zeroes += 1
                    else:
                        min_row_elem = min(min_row_elem, w[row[i]][col[k]])
                if zeroes > 1: min_row_elem = 0
                min_col_elem = math.inf
                zeroes = 0
                for k in range(size):
                    if w[row[k]][col[j]] == 0:
                        zeroes += 1
                    else:
                        min_col_elem = min(min_col_elem, w[row[k]][col[j]])
                if zeroes > 1: 
                    min_col_elem = 0
                if min_row_elem + min_col_elem > mosti:
                    mosti = min_row_elem + min_col_elem
                    row_index = i
                    col_index = j

    return mosti, row_index, col_index


def explore(n, w, edges, cost, row, col, best, fwdptr, backptr, start_time, cutoff, ot):
    global best_cost
    if time.time() - start_time < cutoff:
        colred = [0 for _ in range(n)]
        rowred = [0 for _ in range(n)]
        size = n - edges
        cost += reduce(size, w, row, col, rowred, colred)
        if cost < best_cost:
            if edges == n - 2:
                for i in range(n): best[i] = fwdptr[i]
                if w[row[0]][col[0]] >= math.inf:
                    avoid = 0
                else:
                    avoid = 1
                best[row[0]] = col[1 - avoid]
                best[row[1]] = col[avoid]
                best_cost = cost
                addBestCost(cost, time.time() - start_time, ot)
            else:
                mostv, rv, cv = bestEdge(size, w, row, col)
                lowerbound = cost + mostv
                fwdptr[row[rv]] = col[cv]
                backptr[col[cv]] = row[rv]
                last = col[cv]
                while fwdptr[last] != math.inf: 
                    last = fwdptr[last]
                first = row[rv]
                while backptr[first] != math.inf: 
                    first = backptr[first]
                colrowval = w[last][first]
                w[last][first] = math.inf
                newcol = [math.inf for _ in range(size)]
                newrow = [math.inf for _ in range(size)]
                for i in range(rv): newrow[i] = row[i]
                for i in range(rv, size - 1): newrow[i] = row[i + 1]
                for i in range(cv): newcol[i] = col[i]
                for i in range(cv, size - 1): newcol[i] = col[i + 1]
                explore(n, w, edges + 1, cost, newrow, newcol, best, fwdptr, backptr, start_time, cutoff, ot)
                w[last][first] = colrowval
                backptr[col[cv]] = math.inf
                fwdptr[row[rv]] = math.inf
                if lowerbound < best_cost:
                    w[row[rv]][col[cv]] = math.inf
                    explore(n, w, edges, cost, row, col, best, fwdptr, backptr, start_time, cutoff, ot)
                    w[row[rv]][col[cv]] = 0

        for i in range(size):
            for j in range(size):
                w[row[i]][col[j]] = w[row[i]][col[j]] + rowred[i] + colred[j]


def bnb(w, start_time, cutoff, ot):
    global best_cost
    size = len(w)
    col = [i for i in range(size)]
    row = [i for i in range(size)]
    best = [0 for _ in range(size)]
    route = [0 for _ in range(size)]
    fwdptr = [math.inf for _ in range(size)]
    backptr = [math.inf for _ in range(size)]
    best_cost = math.inf

    explore(size, w, 0, 0, row, col, best, fwdptr, backptr, start_time, cutoff, ot)

    index = 0
    for i in range(size):
        route[i] = index
        index = best[index]
    index = []
    cost = 0

    for i in range(size):
        if i != size - 1:
            src = route[i]
            dst = route[i + 1]
        else:
            src = route[i]
            dst = 0
        cost += w[src][dst]
        index.append([src, dst])
    return cost, index

def Driver(filepath, cutoff):
    temp = filepath.split('.')
    temp = temp[0]
    output_file_sol = temp+"_"+"BnB"+"_"+str(int(cutoff))+".sol"
    output_file_trace = temp+"_"+"BnB"+"_"+str(int(cutoff))+".trace"
    output_sol = open(output_file_sol, 'w')
    output_trace = open(output_file_trace, 'w')
    dimension = 0
    k = 0
    distance_type = ""
    cities = []

    with open(filepath, "r") as input_file:
        isData = False
        line_count = 0
        for line in input_file:
            line = line.strip()
            if ("DIMENSION" in line):
                a = line.split(' ')
                m = a[1]
                dimension = int(m)
                cities = [[0 for i in range(3)] for j in range(dimension)]
            elif ("EDGE_WEIGHT_TYPE" in line):
                a = line.split(' ')
                distance_type = a[1]
            elif ("NODE_COORD_SECTION" in line):
                isData = True
            elif (isData and k < dimension):
                a = line.strip().split(' ')
                cities[k][0] = int(a[0])
                cities[k][1] = float(a[1])
                cities[k][2] = float(a[2])
                k += 1
            line_count += 1
    input_file.closed

    adj_matrix = [[0 for i in range(dimension)] for j in range(dimension)]
    for i in range(dimension):
        for j in range(dimension):
            if i == j:
                adj_matrix[i][j] = math.inf
            else:
                if "EUC_2D" in distance_type:
                    adj_matrix[i][j] = dis_euc(cities[i][1], cities[i][2], cities[j][1], cities[j][2])
                else:
                    adj_matrix[i][j] = dis_geo(cities[i][1], cities[i][2], cities[j][1], cities[j][2])

    start_time = time.time()
    cost, path = bnb(adj_matrix, start_time, cutoff, output_trace)
    output_sol.write(str(cost)+"\n")
    for e in path:
        output_sol.write(str(e[0])+", ")
    output_sol.close()
    output_trace.close()

if __name__ == "__main__":
    Driver("UMissouri.tsp", 2)
