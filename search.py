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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    unvisited = util.Stack()
    visited = set()

    unvisited.push((problem.getStartState(), [])) # (posición del pacman, movimientos)
    # Exploramos por profundidad (LIFO)
    while not unvisited.isEmpty():
        node, actions = unvisited.pop()
        # Si el nodo actual es goalState, devolvemos la lista de movimientos realizados
        if problem.isGoalState(node):
            return actions
        # Solo exploraremos nodos que no hemos explorado aún
        if node not in visited:
            visited.add(node)
            # Miramos los posibles movimientos que podemos realizar
            for nextState, action, actionCost in problem.getSuccessors(node):
                # No nos interesa un nodo que ya ha sido explorado
                if nextState in visited:
                    continue
                unvisited.push((nextState, actions + [action]))

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    unvisited = util.Queue()
    visited = set()

    unvisited.push((problem.getStartState(), [])) # (posición del pacman, movimientos)

    # Exploramos por anchura (FIFO)
    while not unvisited.isEmpty():
        node, actions = unvisited.pop()
        # Si el nodo actual es goalState, devolvemos la lista de movimientos realizados
        if problem.isGoalState(node):
            return actions
        # Solo exploraremos nodos que no hemos explorado aún
        if node not in visited:
            visited.add(node)
            # Miramos los posibles movimientos que podemos realizar
            for nextState, action, actionCost in problem.getSuccessors(node):
                # No nos interesa un nodo que ya ha sido explorado
                if nextState in visited:
                    continue
                unvisited.push((nextState, actions + [action]))

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    '''
    Este ejercicio se ha implementado simplemente para ver si logra pasar el test del autograder.
    '''
    unvisited = util.PriorityQueue()
    visited = set()

    unvisited.push((problem.getStartState(), [], 0), 0) # (posición del pacman, movimientos, coste)
    while not unvisited.isEmpty():
        node, actions, currentCost = unvisited.pop()
        if problem.isGoalState(node):
            return actions
        if node not in visited:
            visited.add(node)
            for successor in problem.getSuccessors(node):
                nextState, action, stepCost = successor
                nextActions = actions + [action]
                nextCost = currentCost + stepCost
                unvisited.push((nextState, nextActions, nextCost), nextCost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    unvisited = util.PriorityQueue()
    minCostToReach = {startState: 0}
    visited = set()

    unvisited.push((startState, [], 0), 0) # ((estado inicial, movimientos, coste), prioridad)
    while not unvisited.isEmpty():
        node, actions, cost = unvisited.pop()
        # Si el estado actual es goalState, devolvemos la lista de movimientos realizados
        if problem.isGoalState(node):
            return actions
        # Solo exploraremos estados que no hemos explorado aún
        if node not in visited:
            visited.add(node)
            # Miramos los posibles movimientos que podemos realizar
            for nextState, action, actionCost in problem.getSuccessors(node):
                nextCost = cost + actionCost
                # Si este estado no se ha explorado o el coste para llegar
                # a este estado es menor a la que hemos explorado anteriormente,
                # entonces lo meteremos en la PriorityQueue
                if nextState not in visited or nextCost < minCostToReach[nextState]:
                    nextActions = actions + [action]
                    # Actualizamos el coste mínimo para alcanzar a este estado
                    minCostToReach[nextState] = nextCost
                    # Calculamos la prioridad según el coste + heuristica
                    priority = nextCost + heuristic(nextState, problem)
                    unvisited.push((nextState, nextActions, nextCost), priority)

    return []

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    unvisited = util.PriorityQueue()
    minCostToReach = {startState: 0}
    visited = set()

    unvisited.push((startState, [], 0), 0) # ((estado inicial, movimientos, coste), prioridad)
    while not unvisited.isEmpty():
        node, actions, cost = unvisited.pop()
        # Si el estado actual es goalState, devolvemos la lista de movimientos realizados
        if problem.isGoalState(node):
            return actions
        # Solo exploraremos estados que no hemos explorado aún
        if node not in visited:
            visited.add(node)
            # Miramos los posibles movimientos que podemos realizar
            for nextState, action, actionCost in problem.getSuccessors(node):
                nextCost = cost + actionCost
                # Si este estado no se ha explorado o el coste para llegar
                # a este estado es menor a la que hemos explorado anteriormente,
                # entonces lo meteremos en la PriorityQueue
                if nextState not in visited or nextCost < minCostToReach[nextState]:
                    nextActions = actions + [action]
                    # Actualizamos el coste mínimo para alcanzar a este estado
                    minCostToReach[nextState] = nextCost
                    # Calculamos la prioridad según el coste + heuristica
                    priority = nextCost + heuristic(nextState, problem)
                    unvisited.push((nextState, nextActions, nextCost), priority)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
