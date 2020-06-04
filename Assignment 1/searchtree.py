import sys

# Data Type definiton for Node of red-black tree
class Node: 
    def __init__(self, key): 
        self.key = key
        self.colour = "Red" #All new nodes are initially red
        self.parent = None
        self.left = None
        self.right = None

# Inital function to check RB tree validity
def checkRB(root):
    return checkRBRecur(root)[0]

# Recursive function checking each node of RB tree recursively and returning
# overall check if true or not
def checkRBRecur(root):
    if root is None: # Base case, if root is None then node is leaf
        return True, 1

    # If the root is red then the tree is not RB
    if((root.parent is None) and (root.colour == "Red")):
        return False, 0

    # If a node is red then both of it's children must be black
    # Also if red then the RB height remains the same
    if (root.colour == "Red"):
        nb = 0
        if ((root.left is not None and (root.left.colour == "Red")) or
            (root.right is not None and (root.right.colour == "Red"))):
            return False, -1
    else:
        nb = 1 # Node is black, therefore add 1 to black-height

    # Recursively check left and right children
    right, nbr = checkRBRecur(root.right)
    left, nbl = checkRBRecur(root.left)

    # Return tuple --> If all recursive returns true then true, otherwise false, and black-height
    return all([right, left, nbr == nbl]), nbr + nb

# Recursively print structure of tree
def structure(root):
    if root is not None:
        if root.parent is not None:
            print(str(root.key) + " , " + root.colour + " P: " + str(root.parent.key))
        else:
            print(str(root.key) + " , " + root.colour) 
        structure(root.left)
        structure(root.right)

# Recursive search function, searches for key
def search(root, key):
    # If root is None then correct toute for key taken but key must not be in tree
    if root is None:
        print("searching for " + str(key) + " - not found")
        return root

    if key < root.key:
        root.left = search(root.left,key)
    elif(key > root.key): 
        root.right = search(root.right, key)
    elif(key == root.key):
        print("searching for " + str(key) + " - found")
    else:
        print("searching for " + str(key) + " - not found")
        
    return root

### Insert Functions
#   insert
#   insertNode
#   findKey
#   rotateRight
#   rotateLeft
#   generateGppCode
#   balance
#   recolour
#   blackRoot
###
def insert(root,key):
    if(root is None):
        root = insertNode(root,None,key)
        root = findKey(root,key)
    else:
        root = insertNode(root,root.parent,key)
        root = findKey(root,key)
    return blackRoot(root)

def insertNode(root, parent, key): 
    if root is None:
        new = Node(key)
        new.parent = parent
        return new 

    if key < root.key: 
        root.left = insertNode(root.left, root, key)
    elif key > root.key: 
        root.right = insertNode(root.right, root, key)
    elif key == root.key:
        return root
        
    return root

def findKey(root,key):
    while(True):
        if(root.left is None and root.right is None):
            return balance(root)
        if key < root.key:
            root = root.left
        elif key > root.key:
            root = root.right
        elif key == root.key: 
            return balance(root)

def rotateRight(root, parent, grandparent, ggpCode):
    subTree = parent.right
    greatGP = grandparent.parent
    grandparent.left = subTree
    if subTree is not None:
        grandparent.left.parent = grandparent
    parent.right = grandparent
    parent.right.parent = parent
    parent.parent = greatGP
    if(ggpCode == 1):
        greatGP.left = parent
    elif(ggpCode == 2):
        greatGP.right = parent
    parent.colour = "Black"
    parent.right.colour = "Red"
    return parent

### ggpCode:
# Need to know if greatgrandparent is None
# and if not none if grandparent is left or right child
# 0 = ggp is None
# 1 = gp is left of ggp
# 2 = gp is right of ggp
def rotateLeft(root, parent, grandparent, ggpCode):
    subTree = parent.left
    greatGP = grandparent.parent
    grandparent.right = subTree
    if subTree is not None:
        grandparent.right.parent = grandparent
    parent.left = grandparent
    parent.left.parent = parent
    parent.parent = greatGP
    if(ggpCode == 1):
        greatGP.left = parent
    elif(ggpCode == 2):
        greatGP.right = parent
    parent.colour = "Black"
    parent.left.colour = "Red"
    return parent

def generateGgpCode(grandparent):
    ggp = grandparent.parent
    if ggp is None:
        return 0
    if ggp.left.key == grandparent.key:
        return 1
    return 2

def balance(root):
    if(root is not None):
        if(root.parent is not None):
            parent = root.parent
            if(root.parent.parent is not None):
                grandparent = root.parent.parent
                if(root.colour == "Red" and parent.colour == "Red" and
                   grandparent.colour == "Black"): # Colour conditions hold
                    #Is root left or right child
                    if(parent.left is not None and parent.left.key == root.key):
                        #Root is left child
                        if(grandparent.left is not None and grandparent.left.key == parent.key):
                            #Parent is left child: Left left case
                            uncle = grandparent.right
                            if(uncle is not None):
                                if(uncle.colour == "Red"):
                                    #Recolour
                                    return balance(recolour(parent,uncle,grandparent))
                            #Rotation
                            ggpCode = generateGgpCode(grandparent)
                            return balance(rotateRight(root,parent,grandparent,ggpCode))
                        else:
                            #Parent is right child: Right left case
                            uncle = grandparent.left
                            if(uncle is not None):
                                if(uncle.colour == "Red"):
                                    #Recolour
                                    return balance(recolour(parent,uncle,grandparent))
                            #Rotation
                            subTree = root.right
                            parent.left = subTree
                            if subTree is not None:
                                parent.left.parent = parent
                            parent.parent = root
                            root.right = parent
                            root.parent = grandparent
                            grandparent.right = root
                            ggpCode = generateGgpCode(grandparent)
                            return balance(rotateLeft(parent, root, grandparent,ggpCode))
                    else:
                        #Root is right child
                        if(grandparent.left is not None and grandparent.left.key == parent.key):
                            #Parent is left child: Left right case
                            uncle = grandparent.right
                            if(uncle is not None):
                                if(uncle.colour == "Red"):
                                    #Recolour
                                    return balance(recolour(parent,uncle,grandparent))
                            #Rotation
                            subTree = root.left
                            if subTree is not None:
                                subTree.parent = parent
                            parent.right = subTree
                            parent.parent = root
                            root.left = parent
                            root.parent = grandparent
                            grandparent.left = root
                            ggpCode = generateGgpCode(grandparent)
                            return balance(rotateRight(parent, root, grandparent,ggpCode))
                        else:
                            #Parent is right child: Right right case
                            uncle = grandparent.left
                            if(uncle is not None):
                                if(uncle.colour == "Red"):
                                    #Recolour
                                    return balance(recolour(parent,uncle,grandparent))
                            #Rotation
                            ggpCode = generateGgpCode(grandparent)
                            return balance(rotateLeft(root,parent,grandparent,ggpCode))

            return balance(parent) #if parent is None
        return root #if root is None

def recolour(p,u,g):
    p.colour = "Black"
    u.colour = "Black"
    g.colour = "Red"
    return g

def blackRoot(root):
    root.colour = "Black"
    return root

### Delete Functions
#   minValueNode
#   maxValueNode
#   deleteNode
#   delete
#   deleteRecur
#   delL
#   delR
#   balL
#   balR
#   fuse
#
###

def delete(root,key):
    if root is None:
        return root
    #elif(key == root.key):
        #return blackRoot(fuse(root))
    #root = deleteNode(root,key)
    return blackRoot(deleteNode(root,key))

# Gets max value node of from left children of root
def minValueNode(root):
    current = root.right
    if current is None:
        return None

    while(current.left is not None): 
        current = current.left  
  
    return current

# Gets min value node of from right children of root
def maxValueNode(root):
    current = root.left
    if current is None:
        return None

    while(current.right is not None): 
        current = current.right
  
    return current


def deleteNode(root, key): 
    if root is None: 
        return root  
 
    if(key < root.key): 
        root.left = deleteNode(root.left, key) 
    elif(key > root.key): 
        root.right = deleteNode(root.right, key) 

    else:
        if(root.colour == "Red"):
            if(root.left is None): 
                temp = root.right
                if(temp is not None):
                    temp.parent = root.parent
                    temp.colour = "Black"
                root = None
                return temp       
            elif(root.right is None): 
                temp = root.left
                if(temp is not None):
                    temp.parent = root.parent
                    temp.colour = "Black"
                root = None
                return temp 

            minRight = minValueNode(root)
            maxLeft = maxValueNode(root)
            if(maxLeft is None):
                root.key = minRight.key
                root.right = deleteNode(root.right , minRight.key)
            else:
                root.key = maxLeft.key
                newColour = maxLeft.colour
                root.left = deleteNode(root.left , maxLeft.key)
            root.colour = maxLeft.colour

        else:
            ### If minRight or maxLeft are Red, replace root and colour Black
            minRight = minValueNode(root)
            maxLeft = maxValueNode(root)
            minRightUsed = False
            if(minRight is not None and minRight.colour == "Red"):
                root.key = minRight.key
                root.colour = "Black"
                minRightUsed = True #to stop double computation and skip elif below
                root.right = deleteNode(root.right , minRight.key)
            elif(maxLeft is not None and maxLeft.colour == "Red" and not minRightUsed):
                root.key = maxLeft.key
                root.colour = "Black"
                root.left = deleteNode(root.left , maxLeft.key)
            else:
                if(maxLeft is not None):
                    return delL(root,key,maxLeft)
                elif(minRight is not None):
                    return delR(root,key,minRight)
                else:
                    return root
                print("Else")
            
    return root

#Left tree is black-height -1 of right tree from current root
def delL(root,key,maxLeft):
    if root is None: 
        return root
    
    if(root.left is not None and root.left.colour == "Red"):
        root.colour = "Red"
        root.left.colour = "Black"
        root.key = maxLeft.key
        root.left = deleteNode(root.left, maxLeft.key)
    elif(root.right is not None and root.right.colour == "Black"):
        root.right.colour = "Red"
        root.key = maxLeft.key
        root.left = balL(deleteNode(root.left, maxLeft.key))
    #elif(root.right is not None and root.right.colour == "Red"):
        
        
    return root

def delR(root,key,minRight):
    if root is None: 
        return root
    
    if(root.right is not None and root.right.colour == "Red"):
        root.colour = "Red"
        root.right.colour = "Black"
        root.key = minRight.key
        root.right = deleteNode(root.right, minRight.key)
    elif(root.left is not None and root.left.colour == "Black"):
        root.left.colour = "Red"
        root.key = minRight.key
        root.right = balR(deleteNode(root.right, minRight.key)) ### Needs balancing
    #elif(root.left is not None and root.left.colour == "Red"):    
        
        
    return root



def balL(root):
    return root

def balR(root):
    return root

#def fuse(root):
#    return fused


def main():

    root = None

    if(len(sys.argv) > 1):
        file = open(sys.argv[1], "r")
    else:
        file = open("textSearch.txt", "r")
        
    for line in file:
        instructions = line.split()
        if(instructions[0] == "insert"):
            root = insert(root,instructions[1])
        elif(instructions[0] == "search"):
            root = search(root,instructions[1])
        elif(instructions[0] == "delete"):
            root = delete(root,instructions[1])
    #structure(root)
    #print(checkRB(root))
    
    
if __name__ == "__main__":
    main()
