# Student Name: Müeyyed ĞARZUDDİN
# Student Number: 1306180132

import copy
import os
import random
import time

goalStateArray = [0, 1, 2, 3, 4, 5, 6, 7, 8]

#  method to clean and clear console
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name=='nt' else 'clear')

#  method to clean and clear console

# Node data structure
class Node:
    def __init__(self, state, parent, operator, depth):
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
    def expand(self):
        states = []
        depth = self.depth + 1
        states.append(Node(self.state.changeToUp(), self, "u", depth))
        states.append(Node(self.state.changeToDown(), self, "d", depth))
        states.append(Node(self.state.changeToLeft(), self, "l", depth))
        states.append(Node(self.state.changeToRight(), self, "r", depth))
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

class StateClass:
    def __init__(self, value):
        self.value = value

    def key(self):
        return ''.join(map(str, self.value))

    # print state
    def print(self):
        print("-------------")
        print("| {} | {} | {} |".format(self.value[0], self.value[1], self.value[2]))
        print("-------------")
        print("| {} | {} | {} |".format(self.value[3], self.value[4], self.value[5]))
        print("-------------")
        print("| {} | {} | {} |".format(self.value[6], self.value[7], self.value[8]))
        print("-------------")

    def toString(self):
        return ' '.join(map(str, self.value))

    # Swap 2 element in array and return new array
    def swap(self, i, j):
        swapedState = self.value.copy()
        temp = swapedState[j]
        swapedState[j] = swapedState[i]
        swapedState[i] = temp
        return StateClass(swapedState)

    # Moves the blank tile up
    def changeToUp(self):
        i = self.value.index(0)
        # forbiden move [first row]
        if i in [0, 1, 2]:
            return None
        return self.swap(i, i - 3)

    # Moves the blank tile down
    def changeToDown(self):
        i = self.value.index(0)
        # forbiden move [last row]
        if i in [6, 7, 8]:
            return None
        return self.swap(i, i + 3)

    # Moves the blank tile left
    def changeToLeft(self):
        i = self.value.index(0)
        # forbiden move [first column]
        if i in [0, 3, 6]:
            return None
        return self.swap(i, i - 1)

    # Moves the blank tile right
    def changeToRight(self):
        i = self.value.index(0)
        # forbiden move [last column]
        if i in [2, 5, 8]:
            return None
        return self.swap(i, i + 1)

    @staticmethod
    # Generate randome solvable state
    def random(cmpx):
        state = StateClass(goalStateArray.copy())
        shuffles = random.randint(10, 10 * cmpx)
        for x in range(shuffles):
            dir = random.randint(0, 4)
            nState = None
            if dir == 0: nState = state.changeToUp()
            if dir == 1: nState = state.changeToDown()
            if dir == 2: nState = state.changeToRight()
            if dir == 3: nState = state.changeToLeft()
            if nState != None: state = nState

        return state

class Solution:
    def __init__(self, isValid, path, depth, expanded, fringe):
        self.isValid = isValid
        self.path = path
        self.depth = depth
        self.expanded = expanded
        self.fringe = fringe

class solverAgent:
    @staticmethod
    def BFS(initState, goalState):
        nodesQueue = []
        visitedStates = {}
        maxFringe = 0
        # add initial node
        nodesQueue.append(Node(copy.deepcopy(initState), None, None, 0))
        while True:
            # empty queue => no solution.
            if len(nodesQueue) == 0:
                return Solution(False, None, None, len(visitedStates), maxFringe)
            # take the node from the front of the queue
            node = nodesQueue.pop(0)

            # save max fringe count
            if len(nodesQueue) > maxFringe:
                maxFringe = len(nodesQueue)

            # check if solution
            if node.state.value == goalState.value:
                return Solution(True, node.path(), len(node.path()), len(visitedStates), maxFringe)

            key = node.state.key()
            isNodeVisited = key in visitedStates
            if isNodeVisited:
                continue

            visitedStates[key] = True

            # Expand the node and add all the expansions to the front of the stack
            nodesQueue.extend(node.expand())

    @staticmethod
    def DFS(initState, goalState):
        return solverAgent.dls(initState, goalState, None)

    @staticmethod
    def dls(initState, goalState, limit=None):
        visitedStates = {}
        nodesStack = []
        maxFringe = 0
        nodesStack.append(Node(copy.deepcopy(initState), None, None, 0))
        while True:
            if len(nodesStack) == 0:
                return Solution(False, None, None, len(visitedStates), maxFringe)

            node = nodesStack.pop(0)

            if len(nodesStack) > maxFringe:
                maxFringe = len(nodesStack)

            if node.state.value == goalState.value:
                path = node.path()
                return Solution(True, path, node.depth, len(visitedStates), maxFringe)

            checkDepth = limit != None
            if checkDepth:
                isDepthReached = node.depth >= limit
                if isDepthReached: continue

            key = node.state.key()
            isNodeVisited = key in visitedStates
            if isNodeVisited and visitedStates[key] <= node.depth:
                continue

            visitedStates[key] = node.depth
            expanded_nodes = node.expand()
            expanded_nodes.extend(nodesStack)
            nodesStack = expanded_nodes

    @staticmethod
    def IDS(initState, goalState, limit=50):
        solution = Solution(False, None, None, 0, 0)
        for i in range(limit):
            result = solverAgent.dls(initState, goalState, i)
            solution.expanded += result.expanded
            if result.fringe > solution.fringe: solution.fringe = result.fringe
            if result.isValid:
                solution.isValid = True
                solution.path = result.path
                solution.depth = result.depth
                return solution

        return solution

endPoint = StateClass(goalStateArray)

# Menu processing
def menu():
    menu = "\nMenu:\n\n"
    menu += "(1) create samples + save in samples.txt \n"
    menu += "(2) load and solve Samples from output.txt \n"
    menu += "(3) get random sample analyzed \n"
    menu += "(0) finish\n"
    while True:
        cls()
        print(menu)
        choice = input(">>> ").lower().rstrip()

        if choice == "1":
            menu_Generate_option()
        elif choice == "2":
            menu_Load_option()
        elif choice == "3":
            menu_Analyzing_option()
        elif choice == "0":
            break
        else:
            print("Invalid option, select again \n")

def menu_Generate_option():
    samples = int(input("enter number of samples that you want : "))
    cmpx = int(input("select sample complexity [1-2-3-4-5-6-7-8-9-10]: "))
    samplesFile = open("samples.txt", "w")
    for i in range(samples):
        sampleState = StateClass.random(cmpx)
        print("sample {} :".format(i + 1))
        sampleState.print()
        samplesFile.write(sampleState.toString() + "\n")
    samplesFile.close()
    print("({}) saved to samples.txt ".format(samples))
    input("Press any key to continue...")

def menu_Load_option():
    if not os.path.isfile("samples.txt"):
        print("./samples.txt file does not exists")
        return

    samplesFile = open("samples.txt", "r")
    outputsFile = open("outputs.txt", "w")

    samples = samplesFile.readlines()

    # function strip to remove spaces
    samples = [x.strip() for x in samples]
    samplesCount = len(samples)

    for i in range(samplesCount):
        sampleText = samples[i]
        sampleState = StateClass([int(x) for x in sampleText.split()])
        print("sample {} :".format(i + 1))
        sampleState.print()

        outputsFile.write("sample {} :\n".format(i + 1))
        outputsFile.write("\tinput: {}\n".format(sampleText))
        outputsFile.write("\tsolutions:\n")

        print("Geting solution by BFS>...", end='')
        generalFunctionForSolution(outputsFile, 'BFS', sampleState, endPoint)
        print("implemented")

        print("Geting solution by DFS>...", end='')
        generalFunctionForSolution(outputsFile, 'DFS', sampleState, endPoint)
        print("implemented")

        print("Geting solution by DLS>...", end='')
        generalFunctionForSolution(outputsFile, 'DLS', sampleState, endPoint, 5)
        generalFunctionForSolution(outputsFile, 'DLS', sampleState, endPoint, 10)
        generalFunctionForSolution(outputsFile, 'DLS', sampleState, endPoint, 15)
        generalFunctionForSolution(outputsFile, 'DLS', sampleState, endPoint, 20)
        generalFunctionForSolution(outputsFile, 'DLS', sampleState, endPoint, 25)
        print("implemented")

        print("Geting solution by IDS>...", end='')
        generalFunctionForSolution(outputsFile, 'IDS', sampleState, endPoint)
        print("implemented")

    samplesFile.close()
    outputsFile.close()
    print("({}) save sample to outputs.txt file.".format(samplesCount))
    input("Press any key to continue...")

def menu_Analyzing_option():
    complexity = int(input("select sample complexity [1-2-3-4-5-6-7-8-9-10]: "))
    print("first state is:\n")
    state = StateClass.random(complexity)
    # state = State([1, 5, 4, 0, 3, 8, 6, 2, 7])
    state.print()

    while True:
        print("Which algorithm you want to select :")
        print("[1]-BFS")
        print("[2]-DFS")
        print("[3]-DLS")
        print("[4]-IDS")
        print("[0]- Back to menu")
        algo = int(input("select algorithm [ 1-2-3-4 ]: "))
        if algo == 0: return
        if algo == 1:
            result = solverAgent.BFS(state, endPoint)
        if algo == 2:
            result = solverAgent.DFS(state, endPoint)
        if algo == 3:
            limit = int(input("Enter the depth limit: "))
            result = solverAgent.dls(state, endPoint, limit)
        if algo == 4:
            result = solverAgent.IDS(state, endPoint)

        if not result.isValid:
            print(" no solution for this state !")
        elif result.path == [None]:
            print("Start node is the goal!")
        else:
            temporary = copy.deepcopy(state)
            print("path: {}".format(' => '.join(result.path)))
            print("depth: {}".format(result.depth))
            print("expandedNodes: {}".format(result.expanded))
            print("fringe: {}".format(result.fringe))
            for i, op in enumerate(result.path):
                if op == 'u': temporary = temporary.changeToUp()
                if op == 'd': temporary = temporary.changeToDown()
                if op == 'r': temporary = temporary.changeToRight()
                if op == 'l': temporary = temporary.changeToLeft()
                print("step {} [{}]:".format(i + 1, op))
                temporary.print()

def generalFunctionForSolution(outputsFile, alg, sampleState, goalState, limit=None):
    start = time.time()
    if alg == 'BFS': sol = solverAgent.BFS(sampleState, goalState)
    if alg == 'DFS': sol = solverAgent.DFS(sampleState, goalState)
    if alg == 'DLS': sol = solverAgent.dls(sampleState, goalState, limit)
    if alg == 'IDS': sol = solverAgent.IDS(sampleState, goalState)
    outputsFile.write("\t\t{}[{}]:\n".format(alg, limit))
    end = time.time()
    if not sol.isValid:
        outputsFile.write("\t\t\tNo solution\n")
        return
    if sol.path == [None]:
        outputsFile.write("\t\t\tInit State same as goal state\n")
        return
    outputsFile.write("\t\t\tlimit: {}\n".format(limit))
    outputsFile.write("\t\t\ttime: {} s\n".format(end - start))
    outputsFile.write("\t\t\tdepth: {}\n".format(sol.depth))
    outputsFile.write("\t\t\texpandedNodes: {}\n".format(sol.expanded))
    outputsFile.write("\t\t\tfringe: {}\n".format(sol.fringe))
    outputsFile.write("\t\t\tpath: {}\n".format(' => '.join(sol.path)))

menu()





