# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    # print "Start:", problem.getStartState()
    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # print "Start's successors:", problem.getSuccessors(problem.getStartState())
    stack = util.Stack()
    node = {}
    nodes_expanded = dict()
    current_position = problem.getStartState()
    #creating a dictionary structure, to keep track of paths visited
    #you need to store parent:V->V,to remember from which cell you got to the current one.
    # This is easily done by storing a dictionary/map, where the key is a cell, and the value is the cell you used to discover the key.
    node["parent_node"] = None
    node["current_position"] = current_position
    node["path"] = None
    stack.push(node)
    # one by one, the node is popped out from the stack, and checked if visited or not
    while not stack.isEmpty(): # Loop till the stack is empty , which means the goal is never found
        node = stack.pop()
        current_position = node["current_position"]
        if nodes_expanded.has_key(hash(current_position)):  # checking if the current_position is visited, if true forcing next iteration
            continue
        nodes_expanded[hash(current_position)] = True      # if not visited , making it visited
        if problem.isGoalState(current_position) == True:
             break
        for child_node in problem.getSuccessors(current_position):
            if not nodes_expanded.has_key(hash(child_node[0])): # if the node is unvisited , create a triplet of info and push it in stack
                childnode = {}
                childnode["parent_node"] = node                   #the prev node is pushed as an info like linked list
                childnode["path"] = child_node[1]
                childnode["current_position"] = child_node[0]
                stack.push(childnode)
    route_traversed = []                             # read the stack and get the directions to the start
    while node["path"] != None:
        route_traversed.insert(0, node["path"])
        node = node["parent_node"]

    return route_traversed

"*** YOUR CODE HERE ***"
def breadthFirstSearch(problem):
    queue = util.Queue()
    current_position = problem.getStartState()
    node = {}
    # creating a dictionary structure, to keep track of paths visited
    # you need to store parent:V->V,to remember from which cell you got to the current one.
    # This is easily done by storing a dictionary/map, where the key is a cell, and the value is the cell you used to discover the key.
    nodes_expanded = dict()
    node["parent_node"] = None
    node["current_position"] = current_position
    node["path"] = None
    queue.push(node)
    # one by one, the node is popped out from the queue, and checked if visited or not
    while not queue.isEmpty():
        node = queue.pop()
        current_position = node["current_position"]
        if nodes_expanded.has_key(hash(current_position)): # checking if the current_position is visited, if true forcing next iteration
            continue
        nodes_expanded[hash(current_position)] = True  # if not visited , making it visited
        if problem.isGoalState(current_position) == True:
            break
        for child in problem.getSuccessors(current_position):
            if not nodes_expanded.has_key(hash(child[0])):
                childnode = {}
                childnode["parent_node"] = node     #the prev node is pushed as an info like linked list
                childnode["path"] = child[1]
                childnode["current_position"] = child[0]
                queue.push(childnode)
    route_traversed = []                             # read the stack and get the directions to the start
    while node["path"] != None:
        route_traversed.insert(0, node["path"])
        node = node["parent_node"]
    return route_traversed
    util.raiseNotDefined()

def uniformCostSearch(problem):
    PriorityQueue = util.PriorityQueue()
    current_position = problem.getStartState()
    # creating a dictionary structure, to keep track of paths visited
    # you need to store parent:V->V,to remember from which cell you got to the current one.
    # This is easily done by storing a dictionary/map, where the key is a cell, and the value is the cell you used to discover the key.
    nodes_expanded = dict()
    node = {}
    node["parent_node"] = None
    node["path"] = None
    node["current_position"] = current_position
    node["cost_value"] = 0
    # Prioty Queue, takes the cost value as the priority number
    PriorityQueue.push(node,node["cost_value"])
    while not PriorityQueue.isEmpty():
        node = PriorityQueue.pop() #The elements are popped out basing on the priority number;i.e cost_value
        current_position = node["current_position"]
        cost_value = node["cost_value"]
        if nodes_expanded.has_key(hash(current_position)):# checking if the current_position is visited, if true forcing next iteration
            continue
        nodes_expanded[hash(current_position)] = True
        if problem.isGoalState(current_position) == True: # if not visited , making it visited
            break
        for child_node in problem.getSuccessors(current_position):
            if not nodes_expanded.has_key(hash(child_node[0])):
                childnode = {}
                childnode["parent_node"] = node       #the prev node is pushed as an info like linked list
                childnode["path"] = child_node[1]
                childnode["current_position"] = child_node[0]
                childnode["cost_value"] = child_node[2]+cost_value
                PriorityQueue.push(childnode,childnode["cost_value"]) # read the priority Queue and get the directions to the start
    route_traversed = []
    while node["path"] != None:
        route_traversed.insert(0, node["path"])
        node = node["parent_node"]
    return route_traversed
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    # creating a dictionary structure, to keep track of paths visited
    # you need to store parent:V->V,to remember from which cell you got to the current one.
    # This is easily done by storing a dictionary/map, where the key is a cell, and the value is the cell you used to discover the key.
    nodeList = {}
    nodes_expanded = dict()
    current_position = problem.getStartState()
    priorityQueue = util.PriorityQueue()
    nodeList["current_position"] = current_position
    nodeList["cost_value"] = 0
    nodeList["parent_node"] = None
    nodeList["path"] = None
    nodeList["heuristic_value"] = heuristic(current_position, problem)# Here the heuristic value, which is the sum of h(n)+c(n) is the priority number
    priorityQueue.push(nodeList, nodeList["cost_value"] + nodeList["heuristic_value"])
    while (priorityQueue):
        nodeList = priorityQueue.pop()
        current_position = nodeList["current_position"]
        costValue = nodeList["cost_value"]
        if nodes_expanded.has_key(current_position):
            continue
        nodes_expanded[current_position] = True # if not visited , making it visited
        if problem.isGoalState(current_position) == True:
            break
        for child_node in problem.getSuccessors(current_position):
            if not nodes_expanded.has_key(child_node[0]):
                childnode = dict()
                childnode["parent_node"] = nodeList
                childnode["current_position"] = child_node[0]
                childnode["path"] = child_node[1]         #the prev node is pushed as an info like linked list
                childnode["cost_value"] = child_node[2] + costValue
                childnode["heuristic_value"] = heuristic(childnode["current_position"], problem)
                priorityQueue.push(childnode, childnode["cost_value"] + childnode["heuristic_value"]) # read the priority Queue and get the directions to the start

    routes = []
    while nodeList["path"] != None:
        routes.insert(0, nodeList["path"])
        nodeList = nodeList["parent_node"]

    return routes
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
