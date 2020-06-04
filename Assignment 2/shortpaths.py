'''
G54PAD Assignment 2

Student:    Alessio Cauteruccio
Email:      psyagca@nottingham.ac.uk
Student ID: 4287379
'''


import sys
import math

# Adjacency List Data Structure
# From i to j with w weight
class ListINode:
    def __init__(self,i,j,w):
        self.i = i
        self.j = ListJNode(j,w,self)
        self.prev = None
        self.next = None

class ListJNode:
    def __init__(self,j,w,prev):
        self.j = j
        self.w = w
        self.prev = prev
        self.next = None

def adjListInsert(root,i,j,w):
    if(root is None):
        return ListINode(i,j,w)
    if(root.i == i):
        #Insert in j's
        root.j = insertJNode(root.j,j,w)
        return root
    elif(root.i < i):
        if(root.next is None):
            new = ListINode(i,j,w)
            root.next = new
            new.prev = root
            return root
        else:
            root.next = adjListInsert(root.next,i,j,w)
    elif(root.i > i):
        if(root.prev is None):
            new = ListINode(i,j,w)
            root.prev = new
            new.next = root
            return new
        else:
            new = ListINode(i,j,w)
            temp = root.prev
            temp.next = new
            new.prev = temp
            new.next = root
            root.prev = new
            return new
    return root

def insertJNode(current,j,w):
    if(current.next is None):
        new = ListJNode(j,w,current)
        current.next = new
        return current
    elif(current.j > j):
        new = ListJNode(j,w,current.prev)
        new.next = current
        current.prev = new
        return new
    elif(current.j == j):
        current.w = w
        return current
    else:
        current.next = insertJNode(current.next,j,w)
    return current

# No weights shown for Adjacency List printing
def printAdjList(root):
    print("\nAdjacency List")
    while root is not None:
        js = root.j
        jString = ""
        while js is not None:
            if js.next is None:
                jString += str(js.j)
            else:
                jString += str(js.j)+", "
            js = js.next
        print(str(root.i)+" --> "+jString)
        root = root.next

def getMatSize(root):
    i = 0
    while root is not None:
        i += 1
        root = root.next
    return i

def getMatMaxElemSize(matrix):
    largest = 0
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if(len(str(matrix[x][y])) > largest):
                largest = len(str(matrix[x][y]))
    return largest

# Converts Adj List into Adj Matrix
# Takes Linked List and creates 2D array
def createAdjMatrix(root):
    size = getMatSize(root)
    matrix = [['-' for i in range(size)] for j in range(size)]
    while root is not None:
        jRoot = root.j
        while jRoot is not None:
            matrix[int(root.i)][int(jRoot.j)] = float(jRoot.w)
            jRoot = jRoot.next
        root = root.next
    return matrix

def printMatrix(matrix):
    largest = getMatMaxElemSize(matrix)
    spacing = [ " "*i for i in reversed(range(largest+4)) ]
    numrows = len(matrix)
    numcols = len(matrix[0])
    firstString = spacing[0]
    for x in range(numcols):
        firstString += str(x)+spacing[len(str(x))]
    print(firstString)
    for x in range(numrows):
        currString = str(x)+spacing[len(str(x))]
        for y in range(numcols):
            currString += str(matrix[x][y])+spacing[len(str(matrix[x][y]))]
        print(currString)
             
def dijkstra(source,size,root):
    # Distance will remain inf until found so won't be expanded until found
    currentDistances = [math.inf for x in range(size)]
    currentDistances[source] = 0.0
    currUnvisitedDistances = [[x,currentDistances[x]] for x in range(size)]
    '''
    Find current shortest found but unvisited node and expand
    '''
    endLoop = len(currUnvisitedDistances)
    #while currUnvisitedDistances: # While unvisited still has nodes in
    while endLoop > 0: # While unvisited still has nodes in
        expandNode = findMinUnvisitedDistance(currUnvisitedDistances)
        # Find children and weight of children of node to expand
        jArray = getJNodes(expandNode[0],root)
        # Check distances with current found distances + current distance of expand node
        while jArray:
            fromSourceDist = expandNode[1] + jArray[0][1]
            currFoundDist = currentDistances[jArray[0][0]]
            # If new distance < old distance replace with new in both currDist arrays
            if(fromSourceDist < currFoundDist):
                currentDistances[jArray[0][0]] = fromSourceDist
                # If unvisited update currUnvisitedDistances
                if jArray[0][0] in [x[0] for x in currUnvisitedDistances]:
                    currUnvisitedDistances[jArray[0][0]] = [jArray[0][0] , fromSourceDist]
            jArray.pop(0)
        # Remove expandNode from currUnvisitedDistances
        currUnvisitedDistances[expandNode[0]] = ['-','-']
        endLoop -= 1
        
    
    printDijkstra(str(source),size,currentDistances)

def findMinUnvisitedDistance(arr):
    currMin = [math.inf,math.inf]
    for x in range(len(arr)):
        if(arr[x][0] != '-'):
            if(arr[x][1] < currMin[1]):
                currMin = arr[x]
    return currMin

# Gets j Nodes from i node and returns array of them
def getJNodes(i,root):
    while(int(i) != int(root.i)):
        root = root.next
    js = root.j
    jArray = []
    while js is not None:
        jArray.append([int(js.j) , float(js.w)])
        js = js.next
    return jArray
        

def printDijkstra(sourceStr,size,distances):
    print("\nDijkstra's Algorithm\nShortest Paths from Source:")
    for x in range(size):
        print(sourceStr +" --> "+str(x)+":  "+str(distances[x]))


def floydWarshall(matrix):
    #Floyd - Warshall Algorithm
    shortMat = matrix
    length = len(matrix)
    for x in range(length):
        for y in range(length):
            if(x == y):
                shortMat[x][y] = 0.0
            if(shortMat[x][y] == '-'):
                shortMat[x][y] = math.inf
    
    for k in range(length): 
        for i in range(length): 
            for j in range(length):  
                shortMat[i][j] = min(shortMat[i][j] , shortMat[i][k] + shortMat[k][j])
    print("\nFloyd-Warshall Algorithm")
    printMatrix(shortMat)    

def main():
    root = None
    
    if(len(sys.argv) > 1):
        file = open(sys.argv[1], "r")
    else:
        file = open("testGraph.txt", "r")

    init = file.read()
    first = init.split("(")
    for x in range(len(first)):
        if first[x] != '':
            new = first[x].split(")")
            splitIJK = new[0].split(",")
            i = splitIJK[0]
            j = splitIJK[1]
            w = splitIJK[2]
            root = adjListInsert(root,i,j,w)

    matrix = createAdjMatrix(root)
    print("Adjacency Matrix")
    printMatrix(matrix)
    dijkstra(0,getMatSize(root),root)
    floydWarshall(matrix)
    
if __name__ == "__main__":
    main()
