import sys

from BnB import Driver
from MSTApprox import MSTApprox
from GA import GA
from SimulatedAnnealing import tsp_sa

def execute():
	filename = sys.argv[2]
	alg = sys.argv[4]
	cutoff = sys.argv[6]
	if "BnB" not in alg and "Approx" not in alg:
		seed = sys.argv[8]

	if "BnB" in alg or "bnb" in alg:
		Driver(filename, float(cutoff))
	elif "Approx" in alg:
		MSTApprox.build_tour(filename, 0, float(cutoff))
	elif "LS1" in alg:
		tsp_sa(filename, float(cutoff), float(seed))
	elif "LS2" in alg:
		GA(filename, float(cutoff), float(seed))

if __name__ == '__main__':
	execute()