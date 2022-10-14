import math


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
        self.root = None
        self.size = 0
        self.alpha = alpha

    def insert(self, user, serverBannedOn, timeOfBan):
        newNode = ScapeGoatNode(user, serverBannedOn, timeOfBan)
        depth = 0
        # if tree empty, the new node will be the root
        if(self.root == None):
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
            if(user < curRoot.user):
                curRoot = curRoot.left
                depth += 1
            elif(user >= curRoot.user):
                curRoot = curRoot.right
                depth += 1

        newNode.parent = prevRoot

        # Now insert the new node
        if(newNode.user < newNode.parent.user):
            newNode.parent.left = newNode
        elif(newNode.user >= newNode.parent.user):
            newNode.parent.right = newNode

        self.size += 1

        # if depth > alphaHeight(tree of size T) find scapegoat and rebalance
        if(depth > self.alphaHeight()):
            # scapeGoat = self.findScapeGoat()
            print("Left off here")
        # To find goat, go backward up list of parents until we find highest imbalanced parent

        # Do in-order traversal of tree starting at the highest imbalanced parent to get arr of sorted vals

        # use values to rebuild tree


    def sizeOfTree(self, node):
        if node is None:
            return 0
        else:
            return self.sizeOfTree(node.left) + self.sizeOfTree(node.right) + 1



    def alphaHeight(self):
        """
        :return: the alpha height of the tree
        """
        return math.floor(math.log(self.size, 1/self.alpha))


    def isAlphaBalanced(self, node):
        """
        check if the tree is alpha balanced by checking the balances of the left and right subtrees
        :param node:
        :return: returns true if balanced, else false
        """
        isLeftBal = self.sizeOfTree(node.left) <= self.alpha * self.sizeOfTree(node)
        isRightBal = self.sizeOfTree(node.right) <= self.alpha * self.sizeOfTree(node)
        return isLeftBal and isRightBal


class AVLTree:
    # def __init__(self):
    #     self.root = None


    def insert(self, root, user, serverBannedOn, timeOfBan):
        # user is key
        if(user < root.user):
            if(root.left):
                beforeBalance = root.left.balance
                root.left = self.insert(root.left, user, serverBannedOn, timeOfBan)
                afterBalance = root.left.balance

                # left subtree changed height
                if(beforeBalance == 0 and afterBalance != 0):
                    root.balance -= 1
                elif(beforeBalance != 0 and afterBalance == 0):
                    root.balance += 1
            else:
                root.left = AVLNode(user, serverBannedOn, timeOfBan)
                root.balance -= 1

        if(root.balance < -1 and root.left.balance <= -1):
            return self.rotRight(root)
        if(root.balance < -1 and root.left.balance >= 1):
            return self.rotLeftRight(root)

        if(user >= root.user):
            if(root.right):
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
        if(newRoot.balance == 0 and (root.left or root.right)):
            newRoot.balance = -1
            root.balance = 1
        elif(newRoot.balance == 0):
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
        if(newRoot.balance == 0 and (root.left or root.right)):
            newRoot.balance = 1
            root.balance = 1
        elif(newRoot.balance == 0):
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




if __name__ == '__main__':
    # SCAPEGOAT AND TEST CASES =========================================

    # =========================================


    # AVL AND TEST CASES =========================================
    # tree = AVLTree()
    # root = None

    # for line in sys.stdin:
    #     line = line.split()

    # if(root == None):
    #     root = AVLNode(10, 0, 0)

    # Left Right case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 5, 0, 0)
    # root = tree.insert(root, 6, 0, 0)

    # Right Left case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 40, 0, 0)
    # root = tree.insert(root, 35, 0, 0)

    # Left Left case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 5, 0, 0)
    # root = tree.insert(root, 4, 0, 0)

    # Right Right case
    # root = tree.insert(root, 20, 0, 0)
    # root = tree.insert(root, 30, 0, 0)
    # root = tree.insert(root, 40, 0, 0)
    # root = tree.insert(root, 50, 0, 0)
    # ==================================================


    # read input from file and insert into a tree ORG ON USER NAME

    # read names from stdin
    print("Hi")

