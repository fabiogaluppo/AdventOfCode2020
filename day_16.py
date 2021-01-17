#python day_16.py < .\input\input16.txt

import sys
import re

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

RED = True
BLACK = False

class IntervalRBNode:
    def __init__(self, low, high, max, red, label):
        self.low = low
        self.high = high
        self.max = max
        self.left = None
        self.right = None
        self.red = red
        self.label = label
    def __str__(self):
        #return "[{}([{}, {}] {}), left: {}, right: {}, max: {}]".format(('RED' if self.red else 'BLACK'), self.low, self.high, self.label, self.left, self.right, self.max)
        return "[([{}, {}] {}), max: {} {}]".format(self.low, self.high, self.label, self.max, ('RED' if self.red else 'BLACK'))
    def __repr__(self):
        return self.__str__()

def maxFromNodes(x):
    return max([x.high, x.left.max if x.left != None else -1, x.right.max if x.right != None else -1])

def rotateLeft(rbnode):
    x = rbnode.right
    rbnode.right = x.left
    x.left = rbnode
    x.red = rbnode.red
    rbnode.red = RED
    x.max = maxFromNodes(x)
    rbnode.max = maxFromNodes(rbnode)
    return x

def rotateRight(rbnode):
    x = rbnode.left
    rbnode.left = x.right
    x.right = rbnode
    x.red = rbnode.red
    rbnode.red = RED
    x.max = maxFromNodes(x)
    rbnode.max = maxFromNodes(rbnode)
    return x

def flipColors(rbnode):
    rbnode.red = not rbnode.red
    rbnode.left.red = not rbnode.left.red
    rbnode.right.red = not rbnode.right.red
    return rbnode

def isLeaf(rbnode):
    return rbnode.left == None and rbnode.right == None

def isRed(rbnode):
    return False if rbnode == None else rbnode.red

class IntervalRBTree:
    def __init__(self, compare = lambda lhs, rhs: rhs - lhs):
        self.root = None
        self.compare = compare    
    def __str__(self):
        return "{}".format(self.root if self.root is not None else 'IntervalRBTree is empty')
    def __repr__(self):
        return self.__str__()    
    def insert(self, low, high, label = ''):
        def adjustCases(rbnode):
            if isRed(rbnode.right) and not(isRed(rbnode.left)):
                rbnode = rotateLeft(rbnode)
            if isRed(rbnode.left) and isRed(rbnode.left.left):
                rbnode = rotateRight(rbnode)
            if isRed(rbnode.left) and isRed(rbnode.right):
                rbnode = flipColors(rbnode)
            rbnode.max = maxFromNodes(rbnode)
            return rbnode
        def insertRec(rbnode, low, high, label):
            if rbnode == None:
                return IntervalRBNode(low, high, high, RED, label)
            cmp = self.compare(rbnode.high, high)
            if cmp < 0:
                rbnode.left = insertRec(rbnode.left, low, high, label)
            elif cmp > 0:
                rbnode.right = insertRec(rbnode.right, low, high, label)
            else:
                cmp = self.compare(rbnode.low, low)
                if cmp < 0:
                    rbnode.left = insertRec(rbnode.left, low, high, label)
                elif cmp > 0:
                    rbnode.right = insertRec(rbnode.right, low, high, label)
                else:
                    return rbnode
            return adjustCases(rbnode) 
        self.root = insertRec(self.root, low, high, label)
        self.root.red = BLACK
    def __overlaps(self, x, i):
        return x.low <= i and i <= x.high
    def search(self, i):
        x = self.root
        while x != None and not self.__overlaps(x, i):
            x = x.left if x.left != None and x.left.max >= i else x.right
        return x
    def __inorderDepthSearchIntervalsRec(self, n, v, acc):
        if n == None:
            return
        self.__inorderDepthSearchIntervalsRec(n.left, v, acc)
        if self.__overlaps(n, v):
            acc.add(n.label)
        self.__inorderDepthSearchIntervalsRec(n.right, v, acc)
    def searchIntervals(self, v):
        acc = set()
        self.__inorderDepthSearchIntervalsRec(self.root, v, acc)
        return acc 

def printTree(rbtree):
    def printTreeRec(rbnode, level):
        spaces = ('_' if isRed(rbnode) else '.').join(['' for  _ in range(2 * level + 1)])
        if rbnode is not None:
            print(spaces + str(rbnode))
            printTreeRec(rbnode.left, level + 1)
            printTreeRec(rbnode.right, level + 1)
        else:
            print(spaces + '_')
    printTreeRec(rbtree.root, 0)

def day16_part1():
    t = IntervalRBTree()
    lines = readAllLines()
    i, j = lines.index("nearby tickets:"), lines.index("your ticket:")
    nearbyTickets = lines[i + 1:]
    fields = lines[:j - 1]
    for field in fields:
        res = re.search("^(.+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$", field)
        t.insert(int(res.group(2)), int(res.group(3)))
        t.insert(int(res.group(4)), int(res.group(5)))
    errorRate = 0
    for line in nearbyTickets:
        for k in line.split(','):
            v = int(k)
            if t.search(v) == None:
                errorRate = errorRate + v
    print(errorRate)

def day16_part2():
    lines = readAllLines()
    i, j = lines.index("nearby tickets:"), lines.index("your ticket:")
    yourTicket = [int(k) for k in lines[j + 1:j + 2][0].split(',')]
    nearbyTickets = lines[i + 1:]
    fields = lines[:j - 1]
    t = IntervalRBTree()

    labels = []
    for field in fields:
        res = re.search("^(.+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$", field)
        label = res.group(1)
        a, b, c, d = int(res.group(2)), int(res.group(3)), int(res.group(4)), int(res.group(5))
        t.insert(a, b, label)
        t.insert(c, d, label)
        labels.append(label)
    
    validTickets = []
    for line in nearbyTickets:
        ok = True
        splittedLine = [int(k) for k in line.split(',')]
        for v in splittedLine:
            if t.search(v) == None:
                ok = False
                break
        if ok:
            validTickets.append(splittedLine)
    
    xss = [] #xss are the columns
    for j in range(len(validTickets[0])):
        intervals = []
        for i in range(len(validTickets)):
            intervals.append(t.searchIntervals(validTickets[i][j]))
        xs = set() #xs are the rows
        for label in labels:
            if all([label in intervalSet for intervalSet in intervals]):
                xs.add(label)
        #DBG
        #print(xs, "count:", len(xs), "index:", j, "\n")
        xss.append((xs, j))
    xss.sort(key = lambda xs: len(xs[0])) #order by count (field set size)
    
    targets = set({"departure location", "departure station", "departure platform", "departure track", "departure date", "departure time"})
    acc = 1
    for i in range(len(xss)):
        index = xss[i][1]
        delta = xss[i][0] - xss[i - 1][0] if i > 0 else xss[i][0]
        if (len(targets & delta) > 0): #if intersection greater than 0
            acc = acc * yourTicket[index]
        print(xss[i][1], delta)
    print()
    print(acc)

if __name__ == "__main__":
    #day16_part1() #Your puzzle answer was 23954.
    day16_part2() #Your puzzle answer was 453459307723.
