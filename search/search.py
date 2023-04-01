# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    dfsStack = util.Stack() #obtain the stack to keep track of the nodes.
    currentS= problem.getStartState()
    corner={}
    corner[currentS]=(("0",("0","0")))
    visited = []
    resultArr = []
    dfsStack.push(currentS)

    while(dfsStack.isEmpty()!=True):
        currentS= dfsStack.pop()
        visited.append(currentS)
        if(problem.isGoalState(currentS)==True):
            while(currentS!=problem.getStartState()):
                resultArr.append(corner.get(currentS)[0])
                currentS= corner.get(currentS)[1]
            ans=[]
            for j in range(resultArr.__len__(),0,-1):
                ans.append(resultArr[j-1])
            return ans


        for k in problem.getSuccessors(currentS):
            val = k[0]
            next = k[1]
            if(visited.__contains__(val)==False):
                dfsStack.push(val)
                corner[val]=(next,currentS)
    return resultArr


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    bfsQueue = util.Queue() #Obtain the datastructure to provide and use to keep track of the nodes.
    
    visited = []
    resultArr = []
    corner = {}
    currentS = problem.getStartState()
    corner[currentS] = (("0",("0","0"))) #Direction, (Coordinates) of the State. 

    bfsQueue.push(currentS)

    while((bfsQueue.isEmpty()==False)):      

        currentS = bfsQueue.pop()
        visited.append(currentS)


        if(problem.isGoalState(currentS)==True):
            while(currentS != problem.getStartState()):
                resultArr.append(corner.get(currentS)[0])
                currentS = corner.get(currentS)[1]
            ans = []
            for j in range(resultArr.__len__(),0,-1):
                ans.append(resultArr[j-1])
            return ans

        for k in problem.getSuccessors(currentS):
            val = k[0]
            next  = k[1]
            if((corner.get(val)==None) and ((visited.__contains__(val))==False)):
                bfsQueue.push(val);
                corner[val]=(next,currentS) 
    return resultArr


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    priorityUCS = util.PriorityQueue()
    currentS = problem.getStartState()
    corner = {}
    corner[currentS] = (("0",("0","0"),0))
    priorityUCS.push(problem.getStartState(),0)
    visited = []
    resultArr = []
    while((priorityUCS.isEmpty()==False)):      
        currentS = priorityUCS.pop()
        visited.append(currentS)
        if(problem.isGoalState(currentS)==True):
            while(currentS != problem.getStartState()):
                resultArr.append(corner.get(currentS)[0])
                currentS = corner.get(currentS)[1]    
            ans = []
            for j in range(resultArr.__len__(),0,-1):
                ans.append(resultArr[j-1])
            return ans
        
        for k in problem.getSuccessors(currentS):
            val = k[0]
            next  = k[1]
            parent =k[2]
            if((corner.get(val)==None) or(corner.get(k[0])[2]) > parent+corner.get(currentS)[2])and ((visited.__contains__(val))==False): 
                priorityUCS.push(val,parent+corner.get(currentS)[2]);
                corner[val]=(next,currentS,(corner.get(currentS)[2]+parent)) 
                
                    
    return resultArr


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    priorityAS = util.PriorityQueue()
   
    visited = []
    resultArr = []
    corner = {}
    currentS = problem.getStartState()
   
    corner[currentS] = (("0",("0","0"),heuristic(currentS, problem)))
    priorityAS.push(currentS,0)

    while((priorityAS.isEmpty()==False)):      
        currentS = priorityAS.pop()
        if(visited.__contains__(currentS)==True):
            continue
        visited.append(currentS)
        if(problem.isGoalState(currentS)==True):
            while(currentS != problem.getStartState()):
                resultArr.append(corner.get(currentS)[0])
                currentS = corner.get(currentS)[1]
           
            ans = []
            for j in range(resultArr.__len__(),0,-1):
                ans.append(resultArr[j-1])
            return ans

        for k in problem.getSuccessors(currentS):
            val = k[0]
            next  = k[1]
            parent = k[2]
            if((corner.get(val)==None) or(corner.get(val)[2]) > parent+corner.get(currentS)[2]) and ((visited.__contains__(val))==False): 
                priorityAS.push(val,(parent+corner.get(currentS)[2] + heuristic(val, problem)));
                corner[val]=(next,currentS,(corner.get(currentS)[2]+parent)) 
                    
    return resultArr


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
