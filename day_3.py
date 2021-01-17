#python day_3.py < .\input\input3.txt

import sys
import functools

def getFromPattern(pattern, index):
    return pattern[(index % len(pattern))]

def readAllLines():
    return [line.rstrip() for line in sys.stdin]

def computeTreesInTheSlope(xs, right, down):
    treeCounter, x = 0, 0
    size = len(xs)
    for y in range(down, size + 1, down):
        if y < size:
            pattern = xs[y]
            x = x + right
            ch = getFromPattern(pattern, x)
            treeCounter = treeCounter + (1 if ch == '#' else 0)
    return treeCounter

def printSlope():
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    xs = readAllLines()
    for right, down in slopes:
        treeCounter, x = 0, 0
        print(right, down)
        size = len(xs)
        for y in list(range(down, size + 1, down)):
            if y < size:
                pattern = xs[y]
                x = x + right
                ch = getFromPattern(pattern, x)
                print(' ' * y, 'O' if ch == '.' else 'X')

def day3_part1():
    right, down = 3, 1
    treeCounter = computeTreesInTheSlope(readAllLines(), right, down)
    print(treeCounter)

def day3_part2():
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    xs = readAllLines()
    ns = [computeTreesInTheSlope(xs, right, down) for right, down in slopes]
    #DBG
    #print(ns)
    treeCounters = functools.reduce(lambda acc, n: acc * n, ns, 1)
    print(treeCounters)

if __name__ == "__main__":
    #day3_part1() #Your puzzle answer was 211.
    day3_part2() #Your puzzle answer was 3584591857.
    #printSlope()
