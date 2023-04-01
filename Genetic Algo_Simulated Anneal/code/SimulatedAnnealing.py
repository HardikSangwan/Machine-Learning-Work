import sys
import math
import random
import time


def aprobfun(d,T):
    if d<=0:
        P=1
    elif d>0:
        P=math.exp(-d/T)
    return P

def dis_euc(x_i,y_i,x_i_1,y_i_1):
    xd = x_i_1-x_i
    yd = y_i_1-y_i
    dist = math.sqrt(xd*xd+yd*yd)
    dist = round(dist)
    return dist

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

def cost(s,dim, dt):
    n=dim
    c = 0
    for i in range(n):
        s_x = s[i][1]
        s_y = s[i][2]
        s_x_1 = s[i+1][1]
        s_y_1 = s[i+1][2]
        if "EUC_2D" in dt:
            dist = dis_euc(s_x,s_y,s_x_1,s_y_1)
        else:
            dist = dis_geo(s_x,s_y,s_x_1,s_y_1)
        c = c+dist
    return c

def exchange2(a,dim):
    n = dim-1
    i,j = random.sample(range(1,n),2)

    a_org=[[0]*3 for _ in range(dim+1)]
    a0=a[i]
    a1 = a[j]
    for k in range(dim+1):
        if k == i:
            a_org[k]=a1
        elif k==j:
            a_org[k]=a0
        else:
            a_org[k]=a[k]
    return a_org

def exchange4(a,dim):
    n = dim-1
    i,j,o,p = random.sample(range(1,n),4)
#    i = random.randint(1,n)
#    j = random.randint(1,n)
#    o = random.randint(1,n)
#    p = random.randint(1,n)
    a_org=[[0]*3 for _ in range(dim+1)]
    a0=a[i]
    a1 = a[j]
    a2 = a[o]
    a3 = a[p]
    for k in range(dim+1):
        if k == i:
            a_org[k]=a1
        elif k==j:
            a_org[k]=a0
        elif k==o:
            a_org[k]=a3
        elif k==p:
            a_org[k]=a2
        else:
            a_org[k]=a[k]
    return a_org

def exchangeall(a,dim):
    a_org=[[0]*3 for _ in range(dim+1)]
    a_org[0]=a[0]
    a_org[dim]=a[dim]
    mid = a[1:dim]
    random.shuffle(mid)
    a_org[1:dim]=mid
    return a_org

def tsp_sa(filepath,co_time,seed):
    # temp = filepath[5:]

    temp = filepath.split('.')
    temp = temp[0]
    output_file_sol = temp+"_"+"sa"+"_"+str(co_time)+"_"+str(seed)+".sol"
    output_file_trace = temp+"_"+"sa"+"_"+str(co_time)+"_"+str(seed)+".trace"
    output_sol = open(output_file_sol, 'w')
    output_trace = open(output_file_trace, 'w')
    test_file = open(filepath,"r")
    line_count = 0
    k=0
    random.seed(seed)
    with test_file:
        for line in test_file:
            #IF it is the first line, we want to grab n and m from it
            if line_count <2:
                line_count=line_count+1
            elif line_count==2:
                a = line.split(' ')
                m = a[1]
                dim = int(m)
                ary = [[0]*3 for _ in range(dim)]
                line_count=line_count+1
            elif line_count==3:
                a = line.split(' ')
                distance_type = a[1]
                line_count=line_count+1
            elif line_count==4:
                line_count=line_count+1
            elif line_count <= dim+4:

                a = line.split(' ')
                ary[k][0]=int(a[0])
                ary[k][1]=float(a[1])
                ary[k][2]=float(a[2])
                k=k+1
                line_count = line_count+1
    row0 = ary[0]
    mid = ary[1:][0:]
    random.shuffle(mid)
    s0=[[0]*3 for _ in range(dim+1)]
    s0[0] = row0
    dd = dim-1
    s0[1:dd]=mid
    s0[dim]=row0
    del(s0[dim+1])
    sbetter = s0
    sbest = s0
    cbest = cost(s0,dim,distance_type)
    c0 = cbest
    str_i='1'
    changeCount=0
    k=0
    kSol=k
    T=1000*dim
    T_int =T
    T_min =1
    b1 = 0.5*T_int
    b2 = 0.25*T_int
    elapsed = 0.0
    output_trace.write( str(elapsed)+ ","+ str(cbest)+"\n")
    start_time = time.clock()
    while  T>T_min and elapsed < co_time:
        if T>=b1:
            snew = exchangeall(sbetter,dim)
        elif T<b1 and T>=b2:
            snew = exchange4(sbetter,dim)
        else:
            snew = exchange2(sbetter,dim)
        cbetter = cost(sbetter,dim,distance_type)
        d = (cost(snew,dim,distance_type)-cbetter)/cbetter
        P = aprobfun(d,T)
        randomfrac = random.random()
        if randomfrac <=P:
            sbetter=snew
            T=0.95*T
            changeCount=changeCount+1
        k = k+1
        if cbetter<cbest:
            cbest=cbetter
            sbest = sbetter
            kSol=k
            elapsed1 = time.clock()-start_time
            output_trace.write( str(round(elapsed1, 2)) + ","+ str(cbest)+"\n")
 #       if randomfrac<=.01:
  #          T=T_int
        elapsed = time.clock()-start_time

    for l in range(1,dim+1):
        str_i=str_i+","+str(sbest[l][0])
    output_sol.write(str(cbest)+"\n")
    output_sol.write(str_i+"\n")
    output_sol.close()
    output_trace.close()
    return cbest,sbest,c0,s0,elapsed
if __name__ == '__main__':
#   uncomment this stuff to allow for it to read in the command line arguements, hard coded this just for debugging purposes
    input_file_path = sys.argv[1]
    #This just grabs the string value and lets us open the file
    input_file = input_file_path[0:]
    print(input_file)
    algo_type = sys.argv[2]
    algo_type = algo_type[0:]
    print(algo_type)
    co_time = sys.argv[3]
    co_time = float(co_time[0:])
    print(co_time)
    seed = sys.argv[4]
    seed = int(seed[0])
#    tourcost = [[0]*10 for _ in range(14)]
#    tourcost_avg = [0]*14
#    elapsed_avg = [0]*14
#    elapsed = [[0]*10 for _ in range(14)]
#    seed_ary = [13, 19, 305, 99, 114, 192, 586, 321, 223, 121]
#    algo_type="sa"
#    co_time=60
#    input = ["data\Atlanta.tsp","data\Berlin.tsp","data\Boston.tsp","data\Champaign.tsp","data\Cincinnati.tsp","data\Denver.tsp","data\NYC.tsp","data\Philadelphia.tsp","data\Roanoke.tsp","data\SanFrancisco.tsp","data\Toronto.tsp","data\UKansasState.tsp","data\ulysses16.tsp","data\UMissouri.tsp"]
#    for j in range(14):
#        input_file = input[j]
#        sum = 0
#        time_sum = 0
#        for i in range(10):
#            seed =seed_ary[i]
#            if algo_type=="sa":
#                tourcost[j][i],tour,int_cost,int_tour,elapsed[j][i] = tsp_sa(input_file,co_time,seed)
#                sum = sum+tourcost[j][i]
#                time_sum = time_sum+elapsed[j][i]
#        tourcost_avg[j] = sum/10
#        elapsed_avg[j] = time_sum/10