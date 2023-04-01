import math
import random
import time
import queue as Q
import os
import glob 

class SequenceScheduler:
    def __init__(self):
        self.destinationStops = []

    def addStop(self, stop):
        self.destinationStops.append(stop)

    def getStop(self, index):
        return self.destinationStops[index]

    def numberOfStops(self):
        return len(self.destinationStops)



class Sequence:
    def __init__(self, sequenceScheduler, sequence=None):
        self.sequenceScheduler = sequenceScheduler
        self.sequence = []
        self.fitness = 0
        self.distance = 0
        if sequence is not None:
            self.sequence = sequence
        else:
            for i in range(0,self.sequenceScheduler.numberOfStops()):
                self.sequence.append(None)

    def generateIndividual(self):
        for stopIndex in range(0, self.sequenceScheduler.numberOfStops()):
            self.setStop(stopIndex, self.sequenceScheduler.getStop(stopIndex))
        random.shuffle(self.sequence)
   
    def getStop(self, sequencePosition):
        return self.sequence[sequencePosition]

    def setStop(self, sequencePosition, stop):
        self.sequence[sequencePosition] = stop
        self.fitness = 0
        self.distance = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1/float(self.getDistance())
        return self.fitness

    def getDistance(self):
        if self.distance == 0:
            sequenceDistance = 0
            for stopIndex in range(0, self.sequenceSize()):
                fromStop = self.getStop(stopIndex)
                destinationStop = None
                if stopIndex+1 < self.sequenceSize():
                    destinationStop = self.getStop(stopIndex+1)
                else:
                    destinationStop = self.getStop(0)
                sequenceDistance += dist_matrix[fromStop][destinationStop]
            self.distance = sequenceDistance
        return self.distance

    def sequenceSize(self):
      return len(self.sequence)

    def containsStop(self, stop):
      return stop in self.sequence


class Population:
    def __init__(self, sequenceScheduler, stopSize, initial):
        self.sequences = []
        self.fittest = None     
        for i in range(0, stopSize):
            self.sequences.append(None)
        if initial: # initial is True at the beginning
            for i in range(0, stopSize):
                newSequence = Sequence(sequenceScheduler)
                newSequence.generateIndividual()
                self.saveSequence(i, newSequence)


    def saveSequence(self, index, sequence):
        self.sequences[index] = sequence

    def getSequence(self, index):
        return self.sequences[index]

    def getFittest(self):
        if self.fittest == None:
            fittest = self.sequences[0]
            for i in range(0, self.populationSize()):
                if fittest.getFitness() <= self.getSequence(i).getFitness():
                    fittest = self.getSequence(i)
            self.fittest = fittest
        return self.fittest

    def populationSize(self):
        return len(self.sequences)

def LCS(parent1, parent2):
    #Longest Common Subsequence: Given two parent sequences,
    # find the length of longest subsequence present in both of them

    size = len(parent1)
    L = []
    row = [] 
    for x in range(0, size+1):
        row.append(0)
        for y in range(0,size+1):
            L.append(row) 
    for i in range(0,size+1):
        for j in range(0,size+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif parent1[i-1] == parent2[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    index = L[size][size]
    lcs = [''] * (index+1)  
    i = size
    j = size
    while i > 0 and j > 0:
        if parent1[i-1] == parent2[j-1]:
            lcs[index-1] = parent1[i-1]             
            index -= 1
            i-=1
            j-=1
        elif L[i-1][j] > L[i][j-1]:
            i-=1
        else:
            j-=1 
    return lcs[0:-1]

def two_OPT(permutation, dist):
    #tow_OPT function is to take a route whice crosses over itself
    # and reorder it so that it is not across.

    n = len(permutation.sequence)
    index1 = -1
    index2 = -1
    best_length_diff = 0
    for i in range(0, n):
        for j in range(i+2, n):
            dist1 = dist[permutation.sequence[i]][permutation.sequence[(i+1)%n]]+dist[permutation.sequence[j]][permutation.sequence[(j+1)%n]]
            dist2 = dist[permutation.sequence[i]][permutation.sequence[j]] + dist[permutation.sequence[(j+1)%n]][permutation.sequence[(i+1)%n]]
            diff = dist1 - dist2
            if diff > best_length_diff:
                best_length_diff = diff
                index1, index2 = i+1, j
    if index1 ==  index2 and index2 == -1:
        return permutation
    permutation.sequence[index1:index2+1] = permutation.sequence[index1:index2+1][::-1]
    return permutation

class GeneticAlgorithm:
    def __init__(self, sequenceScheduler):
        #generate initial population and evaluate the first generation

        self.sequenceScheduler = sequenceScheduler
        self.mutationRate = 0.1 #0.003 initially
        self.crossoverRate = 1 #0.65 initially
        self.elitism = True

    def evolve(self, population):
        #The better visitings in the previous population will be randomly selected.

        newPopulation = Population(self.sequenceScheduler, population.populationSize(), False)
        elitismOffset = 0
        if self.elitism:
            newPopulation.saveSequence(0,population.getFittest())
            elitismOffset = 1
        for i in range(elitismOffset, newPopulation.populationSize()):
            parent1 = self.sequenceSelection(population) #find parent1's fitness
            parent2 = self.sequenceSelection(population) #find parent2's fitness
            parent1 = two_OPT(parent1,dist_matrix) #
            parent2 = two_OPT(parent2,dist_matrix)
            offspring = self.crossover(parent1, parent2)
            self.mutation(offspring)
            newPopulation.saveSequence(i, offspring)
        return newPopulation
    
    def crossover(self,parent1, parent2):
        #CrossOver function: place a random cities which are selected from first parent sequence
        #into offspring sequence and fill unselected cities in the order.

        fitness1 = parent1.fitness
        fitness2 = parent2.fitness
        diff = abs(fitness1-fitness2)
        percent_diff = diff/fitness1
        if percent_diff < 0.01:
            offspring = Sequence(self.sequenceScheduler)
            offspring.generateIndividual()
            return offspring
        r = random.random()
        if r <= self.crossoverRate:
            offspring = Sequence(self.sequenceScheduler)
            common = LCS(parent1.sequence, parent2.sequence)
            c = int(random.random()* parent1.sequenceSize())
            for i in range(0,len(common)):
                offspring.setStop(c, common[i])
                c += 1
                if c == parent1.sequenceSize():
                    c = 0
            j = c
            for i in range(0,offspring.sequenceSize()):
                if not offspring.containsStop(parent1.getStop(i)):
                    offspring.setStop(j,parent1.getStop(i))
                    j += 1
                    if j == parent1.sequenceSize():
                        j = 0
                if not offspring.containsStop(parent2.getStop(i)):
                    offspring.setStop(j,parent2.getStop(i))
                    j += 1
                    if j == parent1.sequenceSize():
                        j = 0

        else:
            r = random.random()
            if r <= 0.5:
                offspring = parent1
            else:
                offspring = parent2
        return offspring

    def mutation(self, sequence):
        # mutatation function: take two cities to visit and swap two cities
        # generate offspring sequence.

        for sequenceIndex1 in range(0, sequence.sequenceSize()):
            if random.random() < self.mutationRate:
                sequenceIndex2 = int(sequence.sequenceSize() * random.random())
                stop1 = sequence.getStop(sequenceIndex1)
                stop2 = sequence.getStop(sequenceIndex2)

                sequence.setStop(sequenceIndex2, stop1)
                sequence.setStop(sequenceIndex1, stop2)

    def sequenceSelection(self, population):
        sequences = Population(self.sequenceScheduler, population.populationSize() , False)
        for i in range(0, population.populationSize()):
            r = int(random.random()*population.populationSize())
            sequences.saveSequence(i, population.getSequence(r))
        fittest = sequences.getFittest()
        return fittest

dist_matrix = {}

def GA(filename, cutofftime, seed):
    #main function of Genetic algorithm

    global dist_matrix
    random.seed(seed)

    sequenceScheduler = SequenceScheduler()
    count = 1
    stops = {}
    decision = True
    with open(filename, 'r') as input_stops:
        for row in input_stops:
            row = row.strip()

            if decision == True:

                row = row.split(': ')
                if row[0] == 'DIMENSION':
                    dimension = int(row[1])
                elif row[0] == 'EDGE_WEIGHT_TYPE':
                    edge_type = row[1]
                elif row[0] == 'NODE_COORD_SECTION':
                    decision = False

            else:
                row = row.split(' ')
                if row[0] == 'EOF':
                    break
                stops[row[0]]= {}
                stops[row[0]]['x'] = float(row[2])
                stops[row[0]]['y'] = float(row[1])
                sequenceScheduler.addStop(row[0])

    
    dist_matrix = {}
    stops_list = list(stops.keys())
    if edge_type == 'EUC_2D':
        for i in range(0,len(stops_list)):
            if stops_list[i] not in dist_matrix:
                dist_matrix[stops_list[i]] = {}
            for j in range(0,len(stops_list)):
                x_diff = abs(stops[stops_list[i]]['x'] - stops[stops_list[j]]['x'])
                y_diff = abs(stops[stops_list[i]]['y'] - stops[stops_list[j]]['y'])
                distance = round(math.sqrt(x_diff*x_diff + y_diff*y_diff)) # x_diff^2+ y_diff^2
                dist_matrix[stops_list[i]][stops_list[j]] = distance
                if stops_list[j] not in dist_matrix:
                    dist_matrix[stops_list[j]]={}
                    dist_matrix[stops_list[j]][stops_list[i]] = distance
    elif edge_type == 'GEO': 
        for i in range(0, len(stops_list)):
            if stops_list[i] not in dist_matrix:
                dist_matrix[stops_list[i]] = {}
            for j in range(0,len(stops_list)):

                PI = 3.141592
                lon_i = stops[stops_list[i]]['x']
                lon_j = stops[stops_list[j]]['x']
                lat_i = stops[stops_list[i]]['y']
                lat_j = stops[stops_list[j]]['y']
                rad_lon_i = PI * (int(lon_i) + 5.0 * (lon_i - int(lon_i)) / 3.0) / 180.0
                rad_lon_j = PI * (int(lon_j) + 5.0 * (lon_j - int(lon_j)) / 3.0) / 180.0
                rad_lat_i = PI * (int(lat_i) + 5.0 * (lat_i - int(lat_i)) / 3.0) / 180.0
                rad_lat_j = PI * (int(lat_j) + 5.0 * (lat_j - int(lat_j)) / 3.0) / 180.0

                RRR = 6378.388
                q1 = math.cos(rad_lon_i - rad_lon_j)
                q2 = math.cos(rad_lat_i - rad_lat_j)
                q3 = math.cos(rad_lat_i + rad_lat_j)
                distance = math.floor(RRR * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0) # x_diff^2+ y_diff^2
                dist_matrix[stops_list[i]][stops_list[j]] = distance
                if stops_list[j] not in dist_matrix:
                    dist_matrix[stops_list[j]]={}
                    dist_matrix[stops_list[j]][stops_list[i]] = distance                

    outputname = filename.split('/')[-1].replace('.tsp', '')
    solfile = filename.split('.')[0] + '_LS1_'+str(cutofftime)+'_'+str(seed)+'.sol'
    soltrace = filename.split('.')[0] + '_LS1_'+str(cutofftime)+'_'+str(seed)+'.trace'

    start = time.time()
    population = Population(sequenceScheduler, 100, True)
    genericAlgorithm = GeneticAlgorithm(sequenceScheduler)
    population = genericAlgorithm.evolve(population)
    bestfit = population.getFittest().getDistance()

    with open(soltrace,'w') as tracefile:
        run_time=time.time()-start
        tracefile.write(str(run_time)+','+str(bestfit)+ '\n')
        while time.time()-start < cutofftime:
            population = genericAlgorithm.evolve(population)
            current_best = population.getFittest().getDistance()
            if current_best < bestfit: #- 0.001
                bestfit = current_best
                run_time=time.time()-start
                tracefile.write(str(run_time)+','+str(bestfit)+ '\n')


    with open(solfile,'w') as solutionfile:
        solutionfile.write(str(population.getFittest().getDistance())+ '\n') #population.getFittest().getDistance()
        tour = population.getFittest().sequence
        for i in range(0,len(tour)):
            if i != len(tour)-1:
                solutionfile.write(tour[i]+',')
            else:
                solutionfile.write(tour[i])
                    

    return filename, run_time, bestfit


import csv


cutoff_time = 5
for file in glob.glob('./DATA/*.tsp'):
    file = file.split('\\')[0] + '/' +file.split('\\')[1] 
    table= [[],[]]
    for seed in range(10):
        A,B,C = GA(file, cutoff_time, seed)
        table[0].append(B)
        table[1].append(C)
        # print table

    with open(file[:-4]+'_'+str(cutoff_time)+'.csv','wb') as tablefile:
        writer=csv.writer(tablefile)
        writer.writerows(table)





