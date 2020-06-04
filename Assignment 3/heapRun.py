'''
G54PAD Assignment 3

Student:    Alessio Cauteruccio
Email:      psyagca@nottingham.ac.uk
Student ID: 4287379
'''
import sys

### Wheel Node Definition     
class WheelNode:
    def __init__(self,key,right,left):
        self.key = key
        self.right = right
        self.left = left
        self.sub = None
        self.parent = None
        self.deg = 0

def isEmptyW(head):
    if head is None:
        return True
    return False

def rightW(head):
    return head.right

def leftW(head):
    return head.left

def insertW(head,key):
    new = WheelNode(key,None,None)
    if(isEmptyW(head)):
        new.right = new
        new.left = new
        return new
    
    newLeft = head.left
    newLeft.right = new
    new.left = newLeft
    newRight = head
    newRight.left = new
    new.right = newRight
    return new

def extractW(head):
    if(head == None):
        return None
    check = rightW(head)
    if(check == head):
        return None
    head.left.right = head.right
    head.right.left = head.left
    return rightW(head)

def printHeap(head,level):
    if(head is not None):
        first = head.key
        print(str(level)+": "+str(head.key)+" "+str(head.deg))
        if(head.sub is not None):
            printHeap(head.sub,level+1)
        head = rightW(head)
        while(head.key != first):
            print(str(level)+": "+str(head.key)+" "+str(head.deg))
            if(head.sub is not None):
                printHeap(head.sub,level+1)
            head = rightW(head)

def concat(loop1Head, loop2Head):
    if loop1Head is None:
        return loop2Head
    elif loop2Head is None:
        return loop1Head

    loop1Left = loop1Head.left
    loop2Left = loop2Head.left

    loop1Head.left = loop2Left
    loop2Left.right = loop1Head
    loop2Head.left = loop1Left
    loop1Left.right = loop2Head

    if loop1Head.key <= loop2Head.key:
        return loop1Head
    else:
        return loop2Head
    

def isEmptyH(head):
    if head is None:
        return True
    return False

def insertH(head,key):
    new = WheelNode(key,None,None)
    if isEmptyH(head):
        new.right = new
        new.left = new
        return new
    
    newLeft = head.left
    newLeft.right = new
    new.left = newLeft
    newRight = head
    newRight.left = new
    new.right = newRight
    if(head.key < new.key):
        return head
    return new

def minimumH(head):
    if head.parent is None:
        return head.key
    else:
        return minimumH(head.parent)

def extractH(head):
    # Remove minimum (head)
    subHead = head.sub
    head = extractW(head)
    # Concatenate head sub-heap into main wheel
    head = concat(head,subHead)
    # Consolidate heap
    head = consolidate(head)
    return head

def consolidate(head):
    head = wheelNA(makeNA(head))
    return head

    
def link(first,second):
    if(first.key <= second.key):
        first.deg += 1
        first.sub = insNode(first.sub,second)
        return first
    else:
        second.deg += 1
        second.sub = insNode(second.sub,first)
        return second
    

def insNA(node,nodeArray):
    if(node.deg >= len(nodeArray)):
        while(node.deg >= len(nodeArray)):
            nodeArray.append(None)
        nodeArray[node.deg] = node
        return nodeArray
    elif(nodeArray[node.deg] == None):
        nodeArray[node.deg] = node
        return nodeArray
    else:
        deg = node.deg
        node = link(node,nodeArray[deg])
        nodeArray[deg] = None
        nodeArray = insNA(node,nodeArray)
    return nodeArray

def makeNA(head):
    nodeArray = []
    if head is not None:
        first = head.key
        nodeArray = insNA(head,nodeArray)
        head = rightW(head)
        while(first != head.key):
            nextN = rightW(head)
            nodeArray = insNA(head,nodeArray)
            head = nextN
    return nodeArray

def wheelNA(nodeArray):
    head = None
    for i in range(len(nodeArray)):
        if(nodeArray[i] is not None):
            head = insNode(head,nodeArray[i])
    return head

def insNode(head,node):
    if head is None:
        node.left = node
        node.right = node
        return node
    newLeft = head.left
    newLeft.right = node
    node.left = newLeft
    newRight = head
    newRight.left = node
    node.right = newRight
    if(head.key < node.key):
        return head
    return node

def main():
    emptyW = None
    emptyH = emptyW
    head = emptyH

    if(len(sys.argv) > 1):
        file = open(sys.argv[1], "r")
    else:
        file = open("heap0.txt", "r")

    init = file.read()
    inputArr = init.split(" ")
    for x in range(len(inputArr)):
        if(inputArr[x] == 'insert'):
            key = int(inputArr[x+1])
            head = insertH(head,key)
        elif(inputArr[x] == 'extract'):
            head = extractH(head)
        elif(inputArr[x] == 'minimum'):
            print("minimum: "+str(minimumH(head)))

if __name__ == "__main__":
    main()
