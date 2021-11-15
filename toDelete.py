# Student Name: Yasser Kamel
# Student Number: 1306180167
# -------------
# | 0 | 1 | 2 |
# -------------
# | 3 | 4 | 5 |
# -------------
# | 6 | 7 | 8 |
# -------------

import sys
import random
import os
import copy
import time


goalStateArray = [0, 1, 2, 3, 4, 5, 6, 7, 8 ]

# Helper method to clear consol
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Node data structure
class Node:
    def __init__( self, state, parent, operator, depth ):
        # State of the node [8 puzzle array]
        self.state = state
        # Node that generated this node [parent node]
        self.parent = parent
        # Contains the operation that generated this node from the parent
        self.operator = operator
        # Depth of this node [from root to node]
        self.depth = depth

    # Generate the 4 possipale stats of the given state
    # Returns a list of nodes
    def expand( self ):
        states = []
        depth = self.depth+1
        states.append( Node( self.state.swapUp(), self, "u", depth))
        states.append( Node( self.state.swapDown(), self, "d", depth))
        states.append( Node( self.state.swapLeft(), self, "l", depth))
        states.append( Node( self.state.swapRight(), self, "r", depth))
        # remove impossible moves (represented ad None)
        return [node for node in states if node.state != None]

    # Print the solution [movements from tree path]
    def path(self):
        moves = []
        temp = self
        while True:
            if temp.operator == None: break
            moves.insert(0, temp.operator)
            if temp.depth == 1: break
            temp = temp.parent
        return moves

class State:
    def __init__( self, value ):
        self.value = value

    def key(self):
        return ''.join(map(str,self.value))

    # print state
    def print( self ):
        print ("-------------")
        print ("| {} | {} | {} |".format(self.value[0], self.value[1], self.value[2]))
        print ("-------------")
        print ("| {} | {} | {} |".format(self.value[3], self.value[4], self.value[5]))
        print ("-------------")
        print ("| {} | {} | {} |".format(self.value[6], self.value[7], self.value[8]))
        print ("-------------")

    def toString(self):
        return ' '.join(map(str,self.value))

    # Swap 2 element in array and return new array
    def swap(self,i,j):
        swapedState = self.value.copy()
        temp = swapedState[j]
        swapedState[j] = swapedState[i]
        swapedState[i] = temp
        return State(swapedState)

    # Moves the blank tile up
    def swapUp( self ):
        i = self.value.index( 0 )
        # forbiden move [first row]
        if i in [0, 1, 2]:
            return None
        return self.swap(i,i-3)

    # Moves the blank tile down
    def swapDown( self ):
        i = self.value.index( 0 )
        # forbiden move [last row]
        if i in [6, 7, 8]:
            return None
        return self.swap(i,i+3)

    # Moves the blank tile left
    def swapLeft( self ):
        i = self.value.index( 0 )
        # forbiden move [first column]
        if i in [0, 3, 6]:
            return None
        return self.swap(i,i-1)

    # Moves the blank tile right
    def swapRight( self ):
        i = self.value.index( 0 )
        # forbiden move [last column]
        if i in [2, 5, 8]:
            return None
        return self.swap(i,i+1)

    @staticmethod
    # Generate randome solvable state
    def random(cmpx):
        state = State(goalStateArray.copy())
        shuffles = random.randint(10, 10 * cmpx)

        for x in range(shuffles):
            dir = random.randint(0, 4)
            nState = None
            if dir == 0: nState = state.swapUp()
            if dir == 1: nState = state.swapDown()
            if dir == 2: nState = state.swapRight()
            if dir == 3: nState = state.swapLeft()
            if nState != None: state = nState

        return state

class Solution:
    def __init__(self,isValid,path,depth,expanded,fringe):
        self.isValid = isValid
        self.path = path
        self.depth = depth
        self.expanded = expanded
        self.fringe = fringe

class NPuzzleAgent:
    @staticmethod
    def bfs( initState, goalState ):
        nodesQueue = []
        visitedStates={}
        maxFringe = 0
        # add initial node
        nodesQueue.append( Node( copy.deepcopy(initState), None, None, 0 ) )
        while True:
            # empty queue => no solution.
            if len( nodesQueue ) == 0:
                return Solution(False,None,None,len(visitedStates),maxFringe)
            # take the node from the front of the queue
            node = nodesQueue.pop(0)

            # save max fringe count
            if len(nodesQueue) > maxFringe:
                maxFringe = len(nodesQueue)

            # check if solution
            if node.state.value == goalState.value:
                return Solution(True,node.path(),len(node.path()),len(visitedStates),maxFringe)

            key = node.state.key()
            isNodeVisited = key in visitedStates
            if isNodeVisited:
                continue

            visitedStates[key] = True

            # Expand the node and add all the expansions to the front of the stack
            nodesQueue.extend( node.expand() )

    @staticmethod
    def dfs( initState, goalState):
        return NPuzzleAgent.dls(initState, goalState, None)

    @staticmethod
    def dls( initState, goalState, limit = None):
        visitedStates={}
        nodesStack = []
        maxFringe = 0
        nodesStack.append( Node( copy.deepcopy(initState), None, None, 0 ) )
        while True:
            if len( nodesStack ) == 0:
                return Solution(False,None,None,len(visitedStates),maxFringe)

            node = nodesStack.pop(0)

            if len(nodesStack) > maxFringe:
                maxFringe = len(nodesStack)

            if node.state.value == goalState.value:
                path = node.path()
                return Solution(True,path,node.depth,len(visitedStates),maxFringe)

            checkDepth = limit != None
            if checkDepth:
                isDepthReached = node.depth >= limit
                if isDepthReached: continue

            key = node.state.key()
            isNodeVisited = key in visitedStates
            if isNodeVisited and visitedStates[key] <= node.depth:
                continue

            visitedStates[key] = node.depth
            expanded_nodes =  node.expand()
            expanded_nodes.extend( nodesStack )
            nodesStack = expanded_nodes

    @staticmethod
    def ids( initState, goalState, limit = 50 ):
        solution = Solution(False,None,None,0,0)
        for i in range( limit ):
            result = NPuzzleAgent.dls( initState, goalState, i )
            solution.expanded += result.expanded
            if result.fringe > solution.fringe: solution.fringe = result.fringe
            if result.isValid :
                solution.isValid = True
                solution.path = result.path
                solution.depth = result.depth
                return solution

        return solution



goalState = State(goalStateArray)

# Menu processing
def menu():

    menu = "\nMenu:\n\n"
    menu += "(G)enerate 8-puzzle samples [to ./samples.txt]\n"
    menu += "(L)oad Samples and solve them [to ./output.txt]\n"
    menu += "(A)nalyze a randomly generated sample\n"
    menu += "(Q)uit\n"
    while True:
        cls()
        print(menu)
        choice = input(">>> ").lower().rstrip()

        if choice == "g": menu_G_option()
        elif choice == "l": menu_L_option()
        elif choice == "a": menu_A_option()
        elif choice == "q": break
        else: print("Invalid choice, please choose again\n")

def menu_G_option():
    samples = int(input("Enter number of samles: "))
    cmpx = int(input("Enter sample complexity [1 to 10]: "))
    samplesFile = open("samples.txt", "w")
    for i in range(samples):
        sampleState = State.random(cmpx)
        print("sample {} :".format(i+1))
        sampleState.print()
        samplesFile.write(sampleState.toString()+"\n")
    samplesFile.close()
    print("({}) Samples are saved to ./samples.txt file.".format(samples))
    input("Press Enter to continue...")

def menu_L_option():
    if not os.path.isfile("samples.txt"):
        print("./samples.txt file does not exists")
        return

    samplesFile = open("samples.txt", "r")
    outputsFile = open("outputs.txt", "w")

    samples = samplesFile.readlines()
    samples = [x.strip() for x in samples]
    samplesCount = len(samples)

    for i in range(samplesCount):
        sampleText = samples[i]
        sampleState = State([int(x) for x in sampleText.split()])
        print("sample {} :".format(i+1))
        sampleState.print()

        outputsFile.write("sample {} :\n".format(i+1))
        outputsFile.write("\tinput: {}\n".format(sampleText))
        outputsFile.write("\tsolutions:\n")

        print("solving with BFS>...", end='')
        hh(outputsFile,'BFS',sampleState, goalState)
        print("Done")

        print("solving with DFS>...", end='')
        hh(outputsFile,'DFS',sampleState, goalState)
        print("Done")

        print("solving with DLS>...", end='')
        hh(outputsFile,'DLS',sampleState, goalState,5)
        hh(outputsFile,'DLS',sampleState, goalState,10)
        hh(outputsFile,'DLS',sampleState, goalState,15)
        hh(outputsFile,'DLS',sampleState, goalState,20)
        hh(outputsFile,'DLS',sampleState, goalState,25)
        print("Done")

        print("solving with IDS>...", end='')
        hh(outputsFile,'IDS',sampleState, goalState)
        print("Done")


    samplesFile.close()
    outputsFile.close()
    print("({}) Samples are solved to ./outputs.txt file.".format(samplesCount))
    input("Press Enter to continue...")

def menu_A_option():
    cmpx = int(input("Enter sample complexity [1 to 10]: "))
    print("The initial state is:\n")
    state = State.random(cmpx)
    #state = State([1, 5, 4, 0, 3, 8, 6, 2, 7])
    state.print()

    while True:
        print("Select the algorithm:")
        print("1-BFS")
        print("2-DFS")
        print("3-DLS")
        print("4-IDS")
        print("0- Back to menu")
        alg = int(input("Enter algorithm number [1 to 4]: "))
        if alg == 0: return
        if alg == 1:
            result = NPuzzleAgent.bfs( state, goalState)
        if alg == 2:
            result = NPuzzleAgent.dfs( state, goalState)
        if alg == 3:
            limit = int(input("Enter the depth limit: "))
            result = NPuzzleAgent.dls( state, goalState, limit )
        if alg == 4:
            result = NPuzzleAgent.ids( state, goalState )

        if not result.isValid:
            print ("The state has no solution!")
        elif result.path == [None]:
            print ("Start node was the goal!")
        else:
            temp = copy.deepcopy(state)
            print ("path: {}".format(' => '.join(result.path)))
            print ("depth: {}".format(result.depth))
            print ("expandedNodes: {}".format(result.expanded))
            print ("fringe: {}".format(result.fringe))
            for i,op in enumerate(result.path):
                if op == 'u': temp = temp.swapUp()
                if op == 'd': temp = temp.swapDown()
                if op == 'r': temp = temp.swapRight()
                if op == 'l': temp = temp.swapLeft()
                print("step {} [{}]:".format(i+1,op))
                temp.print()

def hh(outputsFile, alg, sampleState, goalState, limit=None ):
    start = time.time()
    if alg == 'BFS': sol = NPuzzleAgent.bfs( sampleState, goalState )
    if alg == 'DFS': sol = NPuzzleAgent.dfs( sampleState, goalState )
    if alg == 'DLS': sol = NPuzzleAgent.dls( sampleState, goalState, limit )
    if alg == 'IDS': sol = NPuzzleAgent.ids( sampleState, goalState )
    outputsFile.write("\t\t{}[{}]:\n".format(alg,limit))
    end = time.time()
    if not sol.isValid:
        outputsFile.write("\t\t\tNo solution\n")
        return
    if sol.path == [None]:
        outputsFile.write("\t\t\tInit State same as goal state\n")
        return
    outputsFile.write("\t\t\tlimit: {}\n".format(limit))
    outputsFile.write("\t\t\ttime: {} s\n".format(end-start))
    outputsFile.write("\t\t\tdepth: {}\n".format(sol.depth))
    outputsFile.write("\t\t\texpandedNodes: {}\n".format(sol.expanded))
    outputsFile.write("\t\t\tfringe: {}\n".format(sol.fringe))
    outputsFile.write("\t\t\tpath: {}\n".format(' => '.join(sol.path)))

menu()