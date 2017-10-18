# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()
        score_Food = 0;
        score_Ghost = 0;
        food_distance = 99999
        capsule_distance = 99999
        ghost_distance = 99999
        foodlocations = currentGameState.getFood().asList();
        # current food coordinates of pacman
        for food in foodlocations:
            distance = manhattanDistance(food, newPos)
            if distance < food_distance:
                food_distance = distance
            if distance == 0:
             score_Food = score_Food+100;
            else:
             score_Food = score_Food + 1.0/(distance * distance)

        capsules = currentGameState.getCapsules();
        for capsule in capsules:
            distance = manhattanDistance(capsule, newPos)
            if distance < capsule_distance:
                capsule_distance = distance
            if distance == 0:
                score_Food = score_Food + 100
            else:
                score_Food = score_Food + 10.0/distance

        for ghost in newGhostStates:
            distance = manhattanDistance(ghost.getPosition(), newPos)
            if distance < ghost_distance:
                ghost_distance = distance
            if (distance <=1):
                if (ghost.scaredTimer == 0):
                    score_Ghost = score_Ghost - 200;
                else:
                    score_Ghost = score_Ghost + 2000;

        return score_Food + score_Ghost


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        minmaxScore, minmaxMove = self.maxValues(gameState, self.depth)
        return minmaxMove
        util.raiseNotDefined()

    def maxValues(self, gameState, depth):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), "noMove"

            possibleMoves = gameState.getLegalActions()
            score = [self.minValues(gameState.generateSuccessor(self.index, move), depth, 1) for move in possibleMoves]
            maxScore = max(score)
            maxIndices = [index for index in range(len(score)) if score[index] == maxScore]
            ind = maxIndices[0]
            return maxScore, possibleMoves[ind];

    def minValues(self, gameState, depth, agent):
            if depth == 0 or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState), "noMove"

            possibleMoves = gameState.getLegalActions(agent)
            if (agent != gameState.getNumAgents() - 1):
                score = [self.minValues(gameState.generateSuccessor(agent, move), depth, agent + 1) for move in
                         possibleMoves]
            else:
                score = [self.maxValues(gameState.generateSuccessor(agent, move), (depth - 1)) for move in
                         possibleMoves]

            minScore = min(score)
            minIndices = [index for index in range(len(score)) if score[index] == minScore]
            ind = minIndices[0]
            return minScore, possibleMoves[ind];


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction

        """
        "*** YOUR CODE HERE ***"

        def maxvalue(gameState, alpha, beta, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = -(float("inf"))
            possibleMoves = gameState.getLegalActions()
            for move in possibleMoves:
                nextState = gameState.generateSuccessor(self.index, move)
                v = max(v, minvalue(nextState, alpha, beta, 1, depth))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def minvalue(gameState, alpha, beta, agentindex, depth):
            numghosts = gameState.getNumAgents() - 1
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = float("inf")
            possibleMoves = gameState.getLegalActions(agentindex)
            for move in possibleMoves:
                nextState = gameState.generateSuccessor(agentindex, move)
                if agentindex == numghosts:
                    v = min(v, maxvalue(nextState, alpha, beta, depth - 1))
                    if v < alpha:
                        return v
                    beta = min(beta, v)
                else:
                    v = min(v, minvalue(nextState, alpha, beta, agentindex + 1, depth))
                    if v < alpha:
                        return v
                    beta = min(beta, v)
            return v

        legalActions = gameState.getLegalActions()
        bestaction = Directions.STOP
        score = -(float("inf"))
        alpha = -(float("inf"))
        beta = float("inf")
        for action in legalActions:
            nextState = gameState.generateSuccessor(self.index, action)
            prevscore = score
            score = max(score, minvalue(nextState, alpha, beta, 1, self.depth))
            if score > prevscore:
                bestaction = action
            if score >= beta:
                return bestaction
            alpha = max(alpha, score)
        return bestaction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        value,bestAction  = self.maxValues(gameState, self.depth)

        return bestAction

    def minValues(self, gameState, depth, agents):
        total = len(gameState.getLegalActions(agents))
        average = 0.0
        v = (float("inf"))
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
        for move in gameState.getLegalActions(agents):
            if agents == gameState.getNumAgents() -1:
                v,action=self.maxValues(gameState.generateSuccessor(agents, move), depth - 1)
                average = v+average
            else:
                v = self.minValues(gameState.generateSuccessor(agents, move), depth, agents + 1)
                average = v+average
        return average/total

    def maxValues(self, gameState, depth):
        v = -(float("inf"))
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState),Directions.STOP
        bestAction = Directions.STOP
        for move in gameState.getLegalActions(0):
            prevscore = v
            next = gameState.generateSuccessor(0, move)
            v = max(v, self.minValues(next, depth, 1))
            if (v > prevscore):
                bestAction = move
        return v,bestAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
