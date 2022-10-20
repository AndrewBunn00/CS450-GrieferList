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
            # root = ScapeGoatNode(user, serverBannedOn, timeOfBan)
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
        if (depth > self.alphaHeight()):
            # To find goat, go backward up list of parents until we find highest imbalanced parent
            # set lowest parent as starting point
            highestParent = parentList[-1]
            for i, parent in enumerate(parentList[::-1]):

                if (i > self.alphaHeight(parent)):
                    highestParent = parent

            # Do in-order traversal of tree starting at the highest imbalanced parent to get arr of sorted vals
            subRoot = highestParent
            inOrderNodes = []
            inOrderNodes = self.inOrderTraversal(subRoot, inOrderNodes)
            # TODO figure out why parent is not assigned on certain case... depth 13
            # use inOrderNodes to rebuild tree
            newSubRoot = self.binarySearch(inOrderNodes, 0, len(inOrderNodes) - 1)
            if(highestParent != self.root):
                newSubRoot.parent = highestParent.parent
                highestParent = newSubRoot
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

    def binarySearch(self, inOrderNodes, low, high):
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
            return self.rotRight(root)
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
            return self.rotLeft(root)
        if (root.balance > 1 and root.right.balance <= -1):
            return self.rotRightLeft(root)

        return root

    def rotLeft(self, root):
        newRoot = root.right

        root.right = root.right.left
        newRoot.left = root
        if (newRoot.balance == 0 and (root.left or root.right)):
            newRoot.balance = -1
            root.balance = 1
        elif (newRoot.balance == 0):
            newRoot.balance = -1
            root.balance = 0
        else:
            newRoot.balance = 0
            root.balance = 0

        return newRoot

    def rotRight(self, root):
        newRoot = root.left

        root.left = root.left.right
        newRoot.right = root
        if (newRoot.balance == 0 and (root.left or root.right)):
            newRoot.balance = 1
            root.balance = 1
        elif (newRoot.balance == 0):
            newRoot.balance = 1
            root.balance = 0
        else:
            newRoot.balance = 0
            root.balance = 0

        return newRoot

    def rotLeftRight(self, curNode):
        curNode.left = self.rotLeft(curNode.left)
        return self.rotRight(curNode)

    def rotRightLeft(self, curNode):
        curNode.right = self.rotRight(curNode.right)
        return self.rotLeft(curNode)

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



if __name__ == '__main__':
    # SCAPEGOAT AND TEST CASES =========================================

    # =========================================

    # AVL AND TEST CASES =========================================
    start_time = time.time_ns()

    with open(sys.argv[2]) as file:
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

            with open(sys.argv[3]) as inputFile:
                for line in inputFile.readlines():
                    line = line.split()
                    resList = []
                    tree.isPlayerBanned(root, line[0])


        elif(sys.argv[1] == "scapegoat"):

            tree = ScapeGoatTree(0.9)
            root = None

            for line in file.readlines():
                line = line.split()
                tree.insert(line[0], line[1], line[2])

            with open(sys.argv[3]) as inputFile:
                for line in inputFile.readlines():
                    line = line.split()
                    resList = []
                    tree.isPlayerBanned(line[0])

    time_taken_in_microseconds = (time.time_ns() - start_time) / 1000.0
    print("total time in microseconds: " + str(time_taken_in_microseconds))
    # ==================================================

    # read input from file and insert into a tree ORG ON USER NAME

    # read names from stdin
    # print("Hi")
