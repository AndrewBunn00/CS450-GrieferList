import math
import sys
import time


class ScapeGoatNode:
    def __init__(self, user, serverBannedOn, timeOfBan):
        self.user = user
        self.serverBannedOn = serverBannedOn
        self.timeOfBan = timeOfBan
        self.left = None
        self.right = None
        self.parent = None


class AVLNode:
    def __init__(self, user, serverBannedOn, timeOfBan):
        # user is key
        self.user = user
        self.serverBannedOn = serverBannedOn
        self.timeOfBan = timeOfBan
        self.left = None
        self.right = None
        self.balance = 0


class ScapeGoatTree:
    def __init__(self, alpha):
        self.results = []
        self.root = None
        self.size = 0
        self.alpha = alpha

    def insert(self, user, serverBannedOn, timeOfBan):
        newNode = ScapeGoatNode(user, serverBannedOn, timeOfBan)
        depth = 0
        # if tree empty, the new node will be the root
        if (self.root == None):
            self.size += 1
            self.root = newNode
            return

        curRoot = self.root
        prevRoot = None
        parentList = []

        while curRoot is not None:
            prevRoot = curRoot
            parentList.append(prevRoot)
            # perform bst insert, but track depth and list of parents as we go
            if (user < curRoot.user):
                curRoot = curRoot.left
                depth += 1
            elif (user >= curRoot.user):
                curRoot = curRoot.right
                depth += 1

        newNode.parent = prevRoot

        # Now insert the new node
        if (newNode.user < newNode.parent.user):
            newNode.parent.left = newNode
        elif (newNode.user >= newNode.parent.user):
            newNode.parent.right = newNode

        self.size += 1

        # if depth > alphaHeight(tree of size T) find scapegoat and rebalance
        if (depth > self.alphaHeight() + 1):
            # To find goat, go backward up list of parents until we find highest imbalanced parent
            # set lowest parent as starting point
            highestParent = parentList[-1]
            print("Finding Scapegoat...")
            for i, parent in enumerate(parentList[::-1]):

                if (i > self.alphaHeight(parent)):
                    highestParent = parent
                    break

            # Do in-order traversal of tree starting at the highest imbalanced parent to get arr of sorted vals
            subRoot = highestParent
            inOrderNodes = []
            inOrderNodes = self.inOrderTraversal(subRoot, inOrderNodes)

            # use inOrderNodes to rebuild tree
            listOfNodesToRet = []
            listForInsertion = self.binarySearch(inOrderNodes, 0, len(inOrderNodes) - 1, listOfNodesToRet)
            newSubRoot = listForInsertion[0]

            if(highestParent != self.root):
                newSubRoot.parent = highestParent.parent
                if(highestParent.parent.left == highestParent):
                    highestParent.parent.left = newSubRoot
                else:
                    highestParent.parent.right = newSubRoot
                # highestParent = newSubRoot
            elif(highestParent == self.root):
                self.root = newSubRoot


    def sizeOfTree(self, node):
        if node is None:
            return 0
        else:
            return self.sizeOfTree(node.left) + self.sizeOfTree(node.right) + 1


    def alphaHeight(self, specifiedRoot=None):
        """
        :return: the alpha height of the tree
        """
        if (specifiedRoot is None):
            return math.floor(math.log(self.size, 1 / self.alpha))
        else:
            return math.floor(math.log(self.sizeOfTree(specifiedRoot), 1 / self.alpha))

    def isAlphaBalanced(self, node):
        """
        check if the tree is alpha balanced by checking the balances of the left and right subtrees
        :param node:
        :return: returns true if balanced, else false
        """
        isLeftBal = self.sizeOfTree(node.left) <= self.alpha * self.sizeOfTree(node)
        isRightBal = self.sizeOfTree(node.right) <= self.alpha * self.sizeOfTree(node)
        return isLeftBal and isRightBal

    def inOrderTraversal(self, subRoot, inOrderNodes):
        if (subRoot):
            self.inOrderTraversal(subRoot.left, inOrderNodes)
            inOrderNodes.append(subRoot)
            self.inOrderTraversal(subRoot.right, inOrderNodes)
        return inOrderNodes

    def binarySearch(self, inOrderNodes, low, high, listOfNodesToRet):
        if low > high:
            return

        mid = (low + high) // 2
        newRoot = ScapeGoatNode(inOrderNodes[mid].user, inOrderNodes[mid].serverBannedOn, inOrderNodes[mid].timeOfBan)
        newRoot.left = self.binarySearch(inOrderNodes, low, mid - 1)
        newRoot.right = self.binarySearch(inOrderNodes, mid + 1, high)
        return newRoot


    def getPlayer(self, root, wantedUser):
        # walk the tree and add the found player to the results list
        if (root == None):
            return

        if (root.user == wantedUser):
            self.results.append(root)

        self.getPlayer(root.left, wantedUser)
        self.getPlayer(root.right, wantedUser)


    def isPlayerBanned(self, wantedUser):
        self.getPlayer(tree.root, wantedUser)
        if (len(tree.results) == 0):
            print(f"{wantedUser} is not currently banned from any servers")
        else:
            mostRecentTime = max(node.timeOfBan for node in self.results)
            print(f"{wantedUser} was banned {len(tree.results)} times. "
                  f"Most recently on {mostRecentTime}")
            self.results = []


class AVLTree:
    def __init__(self):
        self.results = []

    def insert(self, root, user, serverBannedOn, timeOfBan):
        # user is key
        if (user < root.user):
            if (root.left):
                beforeBalance = root.left.balance
                root.left = self.insert(root.left, user, serverBannedOn, timeOfBan)
                afterBalance = root.left.balance

                # left subtree changed height
                if (beforeBalance == 0 and afterBalance != 0):
                    root.balance -= 1
                elif (beforeBalance != 0 and afterBalance == 0):
                    root.balance += 1
            else:
                root.left = AVLNode(user, serverBannedOn, timeOfBan)
                root.balance -= 1

        if (root.balance < -1 and root.left.balance <= -1):
            return self.rotRight(root, True)
        if (root.balance < -1 and root.left.balance >= 1):
            return self.rotLeftRight(root)

        if (user >= root.user):
            if (root.right):
                beforeBalance = root.right.balance
                root.right = self.insert(root.right, user, serverBannedOn, timeOfBan)
                afterBalance = root.right.balance

                # right subtree changed height
                if (beforeBalance == 0 and afterBalance != 0):
                    root.balance += 1
                elif (beforeBalance != 0 and afterBalance == 0):
                    root.balance -= 1

            else:
                root.right = AVLNode(user, serverBannedOn, timeOfBan)
                root.balance += 1

        if (root.balance > 1 and root.right.balance >= 1):
            return self.rotLeft(root, True)
        if (root.balance > 1 and root.right.balance <= -1):
            return self.rotRightLeft(root)

        return root


    def rotLeft(self, root, adjBalance):
        if not root.right:
            return root

        newRoot = root.right

        root.right = root.right.left
        newRoot.left = root

        if (adjBalance):
            newRoot.balance = 0
            root.balance = 0

        return newRoot


    def rotRight(self, root, adjBalance):
        if not root.left:
            return root

        newRoot = root.left

        root.left = root.left.right
        newRoot.right = root

        if(adjBalance):
            newRoot.balance = 0
            root.balance = 0

        return newRoot


    def rotLeftRight(self, curNode):
        curNode.left = self.rotLeft(curNode.left, False)
        y = self.rotRight(curNode, False)
        x = y.right
        z = y.left

        if (y.balance == 0):
            x.balance = 0
            z.balance = 0
        else:
            if (y.balance > 0):
                x.balance = -1
                z.balance = 0
            else:
                x.balance = 0
                z.balance = 1
            y.balance = 0
        return y


    def rotRightLeft(self, curNode):
        curNode.right = self.rotRight(curNode.right, False)
        y = self.rotLeft(curNode, False)
        x = y.left
        z = y.right

        if(y.balance == 0):
            x.balance = 0
            z.balance = 0
        else:
            if(y.balance > 0):
                x.balance = -1
                z.balance = 0
            else:
                x.balance = 0
                z.balance = 1
            y.balance = 0
        return y

    def getPlayer(self, root, wantedUser):
        # walk the tree and add the found player to the results list
        if (root == None):
            return

        if (root.user == wantedUser):
            self.results.append(root)

        self.getPlayer(root.left, wantedUser)
        self.getPlayer(root.right, wantedUser)

        # return resList

    def isPlayerBanned(self, root, wantedUser):
        self.getPlayer(root, wantedUser)
        if (len(tree.results) == 0):
            print(f"{wantedUser} is not currently banned from any servers")
        else:
            mostRecentTime = max(node.timeOfBan for node in self.results)
            print(f"{wantedUser} was banned {len(tree.results)} times. "
                  f"Most recently on {mostRecentTime}")
            self.results = []



def readFromStdIn(tree, root=None):
    """
    Reads input from standard in and puts it in lines
    """
    if(root == None):
        for line in sys.stdin:
            line = line.rstrip()
            tree.isPlayerBanned(line)
    else:
        for line in sys.stdin:
            line = line.rstrip()
            tree.isPlayerBanned(root, line)



# Remove \n from lines
def stripEndlines(lines):
    for i, line in enumerate(lines):
        curLine = lines[i].rstrip()  # remove everything that is whitespace at the end of the line
        lines[i] = curLine
    return lines


if __name__ == '__main__':

# AVL AND TEST CASES =========================================
#     tree = AVLTree()
#     root = None

    # for line in sys.stdin:
    #     line = line.split()

    # if(root == None):
    #     root = AVLNode(10, 0, 0)

    # Left Right case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 5, 0, 0)
    # root = tree.insert(root, 6, 0, 0)

    # # Right Left case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 40, 0, 0)
    # root = tree.insert(root, 35, 0, 0)
    #
    # # Left Left case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 5, 0, 0)
    # root = tree.insert(root, 4, 0, 0)
    #
    # # Right Right case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 40, 0, 0)
    # root = tree.insert(root, 50, 0, 0)
    #
    # print("Did i survive")
# ==================================================

    start_time = time.time_ns()

    with open(sys.argv[2], 'r') as file:
        if (sys.argv[1] == "avl"):

            tree = AVLTree()
            root = None

            for line in file.readlines():
                line = line.split()
                if (root == None):
                    # first thing read should be root
                    root = AVLNode(line[0], line[1], line[2])
                else:
                    root = tree.insert(root, line[0], line[1], line[2])

            readFromStdIn(tree, root)



        elif(sys.argv[1] == "scapegoat"):

            tree = ScapeGoatTree(0.75)
            root = None

            for line in file.readlines():
                line = line.split()
                tree.insert(line[0], line[1], line[2])

            readFromStdIn(tree)


    time_taken_in_microseconds = (time.time_ns() - start_time) / 1000.0
    print("total time in microseconds: " + str(time_taken_in_microseconds))

