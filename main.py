import math
import sys
import time


# Implemented: Scapegoat and AVL


class ScapeGoatNode:
    def __init__(self, user, serverBannedOn, timeOfBan):
        self.user = user
        self.serverBannedOn = serverBannedOn
        self.timeOfBan = timeOfBan
        self.left = None
        self.right = None
        self.parent = None
        self.amIRoot = False

class AVLNode:
    def __init__(self, user, serverBannedOn, timeOfBan):
        # user is key
        self.user = user
        self.serverBannedOn = serverBannedOn
        self.timeOfBan = timeOfBan
        self.left = None
        self.right = None
        self.balance = 1

class AVLNode2:
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
            self.root.amIRoot = True
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

            for i, parent in enumerate(parentList[::-1]):

                if (i > self.alphaHeight(parent)):
                    highestParent = parent

            # Do in-order traversal of tree starting at the highest imbalanced parent to get arr of sorted vals
            # subRoot = highestParent
            inOrderNodes = []
            self.inOrderTraversal(highestParent, inOrderNodes)

            # use inOrderNodes to rebuild tree
            listOfNodesToRet = []
            self.binarySearch(inOrderNodes, 0, len(inOrderNodes) - 1, listOfNodesToRet)

            if(highestParent.amIRoot):
                previousRoot = self.root
                self.root = listOfNodesToRet[0]
                self.root.amIRoot = True
                self.root.parent = None

                for i, node in enumerate(listOfNodesToRet):
                    if(i != 0 and not listOfNodesToRet[i].amIRoot):
                        if(listOfNodesToRet[i].parent.left == listOfNodesToRet[i]):
                            listOfNodesToRet[i].parent.left = None
                        else:
                            listOfNodesToRet[i].parent.right = None
                    listOfNodesToRet[i].parent = None
                    listOfNodesToRet[i].left = None
                    listOfNodesToRet[i].right = None # TODO get rid of left and right?

                if previousRoot != self.root:
                    previousRoot.amIRoot = False
                else:
                    previousRoot.amIRoot = True

                # now insert from the subroot
                for i in range(1, len(listOfNodesToRet)):
                    current = self.root
                    insNode = listOfNodesToRet[i]
                    prev = None
                    # newSubRoot = listOfNodesToRet[0]
                    while current is not None:
                        prevRoot = current
                        # perform bst insert, but track depth and list of parents as we go
                        if (insNode.user < current.user):
                            current = current.left
                        elif (insNode.user >= current.user):
                            current = current.right

                    insNode.parent = prevRoot

                    # Now insert the new node
                    if (insNode.user < insNode.parent.user):
                        insNode.parent.left = insNode
                    elif (insNode.user >= insNode.parent.user):
                        insNode.parent.right = insNode
            else:
                previousRoot = self.root
                current = self.root
                isRight = False

                while current != highestParent:
                    if(highestParent.user < current.user):
                        current = current.left
                        isRight = False
                    else:
                        current = current.right
                        isRight = True

                savedParent = current.parent

                for i, node in enumerate(listOfNodesToRet):
                    if (i != 0 and not listOfNodesToRet[i].amIRoot):
                        if (listOfNodesToRet[i].parent.left == listOfNodesToRet[i]):
                            listOfNodesToRet[i].parent.left = None
                        else:
                            listOfNodesToRet[i].parent.right = None
                    listOfNodesToRet[i].parent = None
                    listOfNodesToRet[i].left = None
                    listOfNodesToRet[i].right = None  # TODO get rid of left and right?

                if previousRoot != self.root:
                    previousRoot.amIRoot = False
                else:
                    previousRoot.amIRoot = True

                # reassign the parent
                listOfNodesToRet[0].parent = savedParent

                if isRight:
                    savedParent.right = listOfNodesToRet[0]
                else:
                    savedParent.left = listOfNodesToRet[0]

                for i in range(1, len(listOfNodesToRet)):
                    newCurrent = listOfNodesToRet[0]
                    insNode = listOfNodesToRet[i]
                    prev = None

                    while newCurrent is not None:
                        prev = newCurrent
                        if insNode.user < newCurrent.user:
                            newCurrent = newCurrent.left
                        else:
                            newCurrent = newCurrent.right

                    insNode.parent = prev

                    if(insNode.key < insNode.parent.key):
                        insNode.parent.left = insNode
                    else:
                        insNode.parent.right = insNode





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

    def binarySearch(self, inOrderNodes, low, high, listOfNodesToRet):
        if low > high:
            return

        mid = high - ((high - low) // 2)
        listOfNodesToRet.append(inOrderNodes[mid])

        self.binarySearch(inOrderNodes, low, mid - 1, listOfNodesToRet)
        self.binarySearch(inOrderNodes, mid + 1, high, listOfNodesToRet)
        # return listOfNodesToRet


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


    def fillOutRecords(self, root, playerRecords):
        if(root is None):
            return

        self.fillOutRecords(root.left, playerRecords)

        if(root.user in playerRecords):
            list = playerRecords.get(root.user)
            if int(list[1]) < int(root.timeOfBan):
                list[1] = root.timeOfBan
            list[0] += 1
            playerRecords[root.user] = list
        else:
            playerRecords[root.user] = [1, root.timeOfBan]
        self.fillOutRecords(root.right, playerRecords)
        return playerRecords





class AVLTree:
    def __init__(self):
        self.results = []
        self.root = None

    # def insert(self, root, user, serverBannedOn, timeOfBan):
    #     # user is key
    #     if (user < root.user):
    #         if (root.left):
    #             beforeBalance = root.left.balance
    #             root.left = self.insert(root.left, user, serverBannedOn, timeOfBan)
    #             afterBalance = root.left.balance
    #
    #             # left subtree changed height
    #             if (beforeBalance == 0 and afterBalance != 0):
    #                 root.balance -= 1
    #             # elif (beforeBalance != 0 and afterBalance == 0):
    #             #     root.balance += 1
    #         else:
    #             root.left = AVLNode(user, serverBannedOn, timeOfBan)
    #             root.balance -= 1
    #
    #     if (root.balance < -1 and root.left.balance <= -1):
    #         return self.rotRight(root, True)
    #     if (root.balance < -1 and root.left.balance >= 1):
    #         return self.rotLeftRight(root)
    #
    #     if (user >= root.user):
    #         if (root.right):
    #             beforeBalance = root.right.balance
    #             root.right = self.insert(root.right, user, serverBannedOn, timeOfBan)
    #             afterBalance = root.right.balance
    #
    #             # right subtree changed height
    #             if (beforeBalance == 0 and afterBalance != 0):
    #                 root.balance += 1
    #             # elif (beforeBalance != 0 and afterBalance == 0):
    #             #     root.balance -= 1
    #
    #         else:
    #             root.right = AVLNode(user, serverBannedOn, timeOfBan)
    #             root.balance += 1
    #
    #     if (root.balance > 1 and root.right.balance >= 1):
    #         return self.rotLeft(root, True)
    #     if (root.balance > 1 and root.right.balance <= -1):
    #         return self.rotRightLeft(root)
    #
    #     return root
    #
    #
    # def rotLeft(self, root, adjBalance):
    #     if not root.right:
    #         return root
    #
    #     newRoot = root.right
    #
    #     root.right = root.right.left
    #     newRoot.left = root
    #
    #     if (adjBalance):
    #         newRoot.balance = 0
    #         root.balance = 0
    #
    #     return newRoot
    #
    #
    # def rotRight(self, root, adjBalance):
    #     if not root.left:
    #         return root
    #
    #     newRoot = root.left
    #
    #     root.left = root.left.right
    #     newRoot.right = root
    #
    #     if(adjBalance):
    #         newRoot.balance = 0
    #         root.balance = 0
    #
    #     return newRoot
    #
    #
    # def rotLeftRight(self, curNode):
    #     curNode.left = self.rotLeft(curNode.left, False)
    #     y = self.rotRight(curNode, False)
    #     x = y.right
    #     z = y.left
    #
    #     if (y.balance == 0):
    #         x.balance = 0
    #         z.balance = 0
    #     else:
    #         if (y.balance > 0):
    #             x.balance = -1
    #             z.balance = 0
    #         else:
    #             x.balance = 0
    #             z.balance = 1
    #         y.balance = 0
    #     return y
    #
    #
    # def rotRightLeft(self, curNode):
    #     curNode.right = self.rotRight(curNode.right, False)
    #     y = self.rotLeft(curNode, False)
    #     x = y.left
    #     z = y.right
    #
    #     if(y.balance == 0):
    #         x.balance = 0
    #         z.balance = 0
    #     else:
    #         if(y.balance > 0):
    #             x.balance = -1
    #             z.balance = 0
    #         else:
    #             x.balance = 0
    #             z.balance = 1
    #         y.balance = 0
    #     return y

    # ====================================================
    # def insert(self, rt, user, serverBannedOn, timeOfBan):
    #     insNode = AVLNode(user, serverBannedOn, timeOfBan)
    #     # begin insert
    #     if rt is None:
    #         return insNode
    #     elif(user < rt.user):
    #         rt.left = self.insert(rt.left, user, serverBannedOn, timeOfBan)
    #     elif(user >= rt.user):
    #         rt.right = self.insert(rt.right, user, serverBannedOn, timeOfBan)
    #
    #     # Update height (Add 1 for root)
    #     rt.balance = max(self.getHeight(rt.left), self.getHeight(rt.right)) + 1
    #     balanceFactor = self.getBalance(rt)
    #
    #     if(balanceFactor > 1):
    #         # Left left
    #         if(self.getBalance(rt.left) == 1):
    #             rt = self.rotLeft(rt)
    #
    #         # Left right
    #         else:
    #             rt.left = self.rotRight(rt.left)
    #             rt = self.rotLeft(rt)
    #
    #     elif(balanceFactor < -1):
    #         # Right right
    #         if(self.getBalance(rt.right) == -1):
    #             rt = self.rotRight(rt)
    #
    #         # Right Left
    #         else:
    #             rt.right = self.rotLeft(rt.right)
    #             rt = self.rotRight(rt)
    #
    #     # else it is balanced
    #     return rt


    # def getBalance(self, root):
    #     if not root:
    #         return 0
    #
    #     return(self.getHeight(root.left) - self.getHeight(root.right))
    #
    #
    # def getHeight(self, root):
    #     if not root:
    #         return -1
    #     return root.balance
    #
    #
    # def rotLeft(self, rt):
    #     c = rt.left
    #     rt.left = c.right
    #     c.right = rt
    #     rt.height = max(self.getHeight(rt.left), self.getHeight(rt.right)) + 1
    #     c.height = max(self.getHeight(c.left), self.getHeight(c.right)) + 1
    #     return c
    #
    #
    # def rotRight(self, rt):
    #     c = rt.right
    #     rt.right = c.left
    #     c.left = rt
    #     rt.height = max(self.getHeight(rt.left), self.getHeight(rt.right)) + 1
    #     c.height = max(self.getHeight(c.left), self.getHeight(c.right)) + 1
    #     return c

    # ====================================================
    def insert(self,  root, user, serverBannedOn, timeOfBan):
        if root is None:
            return AVLNode(user, serverBannedOn, timeOfBan)
        elif(user < root.user):
            root.left = self.insert(root.left, user, serverBannedOn, timeOfBan)
        else:
            root.right = self.insert(root.right, user, serverBannedOn, timeOfBan)

        # Need to update the root balance (trying to keep height instead to use for balance factor)
        root.balance = max(self.height(root.left), self.height(root.right)) + 1

        # Now get the balance based on the heights of the subtrees
        bal = self.balance(root)

        # LL
        if((bal > 1)):
            if((user < root.left.user)):
                return self.rotRight(root)
            elif(user > root.left.user):
                root.left = self.rotLeft(root.left)
                return self.rotRight(root)

        if((bal < -1)):
            if(user > root.right.user):
                return self.rotLeft(root)
            elif(user < root.right.user):
                root.right = self.rotRight(root.right)
                return self.rotLeft(root)

        # if(bal > 1 and user > root.left.user):
        #     root.left = self.rotLeft(root.left)
        #     return self.rotRight(root)

        # if(bal < -1 and user < root.right.user):
        #     root.right = self.rotRight(root.right)
        #     return self.rotLeft(root)

        return root


    def rotRight(self, root):
        left = root.left
        lRight = left.right

        left.right = root
        root.left = lRight

        root.balance = max(self.height(root.left), self.height(root.right))
        left.balance = max(self.height(left.left), self.height(left.right))

        return left

    def rotLeft(self, root):
        right = root.right
        t = right.left

        right.left = root
        root.right = t

        root.balance = max(self.height(root.left), self.height(root.right))
        right.balance = max(self.height(right.left), self.height(right.right))

        return right

    def height(self, root):
        if root is None:
            return 0

        return root.balance

    def balance(self, root):
        if root is None:
            return 0

        return self.height(root.left) - self.height(root.right)

    # ====================================================

    def getPlayer(self, root, wantedUser):
        # walk the tree and add the found player to the results list
        if (root == None):
            return

        if (root.user == wantedUser):
            self.results.append(root)

        self.getPlayer(root.left, wantedUser)
        self.getPlayer(root.right, wantedUser)

        # return resList

    # def isPlayerBanned(self, root, wantedUser):
    #     self.getPlayer(root, wantedUser)
    #     if (len(tree.results) == 0):
    #         print(f"{wantedUser} is not currently banned from any servers")
    #     else:
    #         mostRecentTime = max(node.timeOfBan for node in self.results)
    #         print(f"{wantedUser} was banned {len(tree.results)} times. "
    #               f"Most recently on {mostRecentTime}")
    #         self.results = []

    def isPlayerBanned(self, wantedUser, playerRecords=None):
        self.getPlayer(tree.root, wantedUser)
        if (len(tree.results) == 0):
            print(f"{wantedUser} is not currently banned from any servers.")
        else:
            mostRecentTime = max(node.timeOfBan for node in self.results)
            print(f"{wantedUser} was banned from {len(tree.results)} servers. "
                  f"most recently on: {mostRecentTime}")
            self.results = []



def readFromStdIn(tree, playerRecords=None, root=None):
    """
    Reads input from standard in and puts it in lines
    """
    if playerRecords == None:
        if(root == None):
            for line in sys.stdin:
                line = line.rstrip()
                tree.isPlayerBanned(line)
        else:
            for line in sys.stdin:
                line = line.rstrip()
                tree.isPlayerBanned(line)

    else:
        if (root == None):
            for line in sys.stdin:
                line = line.rstrip()
                line = line.split()
                if(playerRecords.get(line[0]) is None):
                    print(f"{line[0]} is not currently banned from any servers.")
                else:
                    print(f"{line[0]} was banned from {playerRecords[line[0]][0]} servers. "
                          f"most recently on: {playerRecords[line[0]][1]}")

        # else:
        #     for line in sys.stdin:
        #         line = line.rstrip()
        #         line = line.split()
        #         if(playerRecords.get(line[0]) is None):
        #             print(f"{line[0]} is not currently banned from any servers")
        #         else:
        #             print(f"{line[0]} was banned {playerRecords[line][0]} times. "
        #                   f"Most recently on {playerRecords[line][1]}")



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
    # root = tree.insert(root, 10, 0, 0)
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

    # print("Did i survive")
# ==================================================

    start_time = time.time_ns()

    with open(sys.argv[2], 'r') as file:
        if (sys.argv[1] == "avl"):

            tree = AVLTree()
            # root = None

            for line in file.readlines():
                line = line.split()
                # if (root == None):
                #     # first thing read should be root
                #     root = AVLNode(line[0], line[1], line[2])
                # else:
                tree.root = tree.insert(tree.root, line[0], line[1], line[2])

            readFromStdIn(tree)



        elif(sys.argv[1] == "scapegoat"):
            # Give tree alpha val
            tree = ScapeGoatTree(0.79)
            root = None
            playerRecords = dict()

            # Build the tree
            for line in file.readlines():
                line = line.split()
                tree.insert(line[0], line[1], line[2])

            # Get all the players in the map
            playerRecords = tree.fillOutRecords(tree.root, playerRecords)

            # Read all the potentially banned players and find if they are or not (print out)
            readFromStdIn(tree, playerRecords)


    time_taken_in_microseconds = (time.time_ns() - start_time) / 1000.0
    print("total time in microseconds: " + str(time_taken_in_microseconds))

