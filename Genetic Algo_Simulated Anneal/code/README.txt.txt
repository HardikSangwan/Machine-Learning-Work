Group 3 Project

TO RUN:

USING PYTHON 3.7+: 

1. copy <instance>.tsp file into the same directory as the Python files (Driver.py, BnB.py, etc)
2. make sure numpy is installed or install by running: 
	pip install numpy 
(pip comes packaged with Python 3.7+)
3. run Driver program by running:
	Driver.py -inst <filename> -alg [BnB | Approx | LS1 | LS2] -time <cutoff_in_seconds> [-seed <random_seed>]
	NOTE: the Approx flag uses MST Approx algorithm, the LS1 flag uses the Simulated Annealing Algorithm, and the LS2 flag uses the Genetic Algorithm.
4. Output files should be present in the current directory.